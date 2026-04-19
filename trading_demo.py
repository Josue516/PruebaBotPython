"""
Módulo principal de la simulación de trading con la API de Alpaca.
Orquesta la descarga de datos, análisis técnico, gestión de riesgo y ejecución de órdenes.
"""
import os
import yfinance as yf
import pandas as pd
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from analista import calcular_indicadores, calcular_senal
from gestor_riesgo import validar_orden

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

def obtener_datos():
    """Descarga datos históricos de AMZN (1 año, intervalo 1h) desde Yahoo Finance."""
    data = yf.download("AMZN", period="1y", interval="1h")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data.dropna(how='all', inplace=True)
    print(f"Datos descargados: {len(data)} filas.")
    return data

def graficar(data):
    """Grafica el precio de cierre, las medias móviles y las señales de compra/venta."""
    data['Signal'] = 0
    data.loc[data['MA20'] > data['MA50'], 'Signal'] = 1
    data.loc[data['MA20'] < data['MA50'], 'Signal'] = -1
    data['Position'] = data['Signal'].diff()

    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Precio de Cierre', alpha=0.5)
    plt.plot(data['MA20'], label='MA20')
    plt.plot(data['MA50'], label='MA50')

    plt.plot(
        data[data['Position'] == 1].index,
        data['MA20'][data['Position'] == 1],
        '^', markersize=10, label='Compra'
    )
    plt.plot(
        data[data['Position'] == -1].index,
        data['MA20'][data['Position'] == -1],
        'v', markersize=10, label='Venta'
    )

    plt.title("Estrategia Cruce de Medias Móviles")
    plt.legend()
    plt.grid()
    plt.show()

def ejecutar_trade(senal, cantidad):
    """Ejecuta una orden de compra o venta en Alpaca según la señal recibida."""
    posiciones = api.list_positions()
    tengo_posicion = any(p.symbol == "AMZN" for p in posiciones)

    if senal == 1 and not tengo_posicion:
        print(f"Ejecutando COMPRA de {cantidad} acciones...")
        api.submit_order(symbol="AMZN", qty=cantidad, side="buy",
                         type="market", time_in_force="gtc")
    elif senal == -1 and tengo_posicion:
        print(f"Ejecutando VENTA de {cantidad} acciones...")
        api.submit_order(symbol="AMZN", qty=cantidad, side="sell",
                         type="market", time_in_force="gtc")
    elif senal == 1 and tengo_posicion:
        print("Sin acción: ya tienes posición abierta.")
    elif senal == -1 and not tengo_posicion:
        print("Sin acción: no tienes posición para vender.")
    else:
        print("Sin señal de trading.")

# --- MAIN ---
if __name__ == "__main__":
    data = obtener_datos()
    data = calcular_indicadores(data)
    graficar(data)

    senal = calcular_senal(data)
    precio_actual = float(data['Close'].iloc[-1])

    cuenta = api.get_account()
    saldo = float(cuenta.cash)

    cantidad, stop_loss = validar_orden(precio_actual, saldo)

    print(f"Señal: {senal} | Precio: {precio_actual:.2f} | Cantidad: {cantidad} | Stop Loss: {stop_loss:.2f}")
    ejecutar_trade(senal, cantidad)
