"""
Módulo principal de la simulación de trading con la API de Alpaca.
Orquesta la descarga de datos, análisis técnico, gestión de riesgo y ejecución de órdenes.
"""
import os
import yfinance as yf
import pandas as pd
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dotenv import load_dotenv
from analista import calcular_indicadores, calcular_senal, historial_cruces, calcular_senales
from gestor_riesgo import validar_orden

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')



def obtener_datos(simbolo):
    """Descarga datos históricos de un activo."""
    data = yf.download(simbolo, period="3mo", interval="1h")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data.dropna(how='all', inplace=True)

    print(f"{simbolo}: {len(data)} filas descargadas.")
    return data


def graficar(data, simbolo, ax):
    """Grafica el precio, medias móviles y señales en un eje dado."""

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # Mostramos solo mes-día en el grafico
    ax.plot(data['Close'], label='Precio', alpha=0.5)
    ax.plot(data['MA20'], label='MA20')
    ax.plot(data['MA50'], label='MA50')

    ax.plot(
        data[data['Position'] == 1].index,
        data['MA20'][data['Position'] == 1],
        '^', markersize=8, label='Compra'
    )

    ax.plot(
        data[data['Position'] == -1].index,
        data['MA20'][data['Position'] == -1],
        'v', markersize=8, label='Venta'
    )

    ax.set_title(simbolo)
    ax.legend()
    ax.grid()

def ejecutar_trade(simbolo, senal, cantidad):
    """Ejecuta una orden de compra o venta en Alpaca según la señal recibida."""
    
    posiciones = api.list_positions()
    tengo_posicion = any(p.symbol == simbolo for p in posiciones)

    if senal == 1 and not tengo_posicion:
        print(f"Ejecutando COMPRA de {cantidad} acciones de {simbolo}...")
        api.submit_order(
            symbol=simbolo,
            qty=cantidad,
            side="buy",
            type="market",
            time_in_force="gtc"
        )

    elif senal == -1 and tengo_posicion:
        print(f"Ejecutando VENTA de {cantidad} acciones de {simbolo}...")
        api.submit_order(
            symbol=simbolo,
            qty=cantidad,
            side="sell",
            type="market",
            time_in_force="gtc"
        )

    elif senal == 1 and tengo_posicion:
        print(f"{simbolo}: ya tienes posición abierta.")

    elif senal == -1 and not tengo_posicion:
        print(f"{simbolo}: no tienes posición para vender.")

    else:
        print(f"{simbolo}: sin señal de trading.")

# --- MAIN ---
#Hay que recordar siempre mantener el orden al ejecutar las funciones, ya me dieron varios errores por eso...
if __name__ == "__main__":
    simbolos = ["AMZN", "AAPL", "MSFT"]
    fig, axes = plt.subplots(1, len(simbolos), figsize=(15, 5))

    for i, simbolo in enumerate(simbolos):
        print(f"\n--- {simbolo} ---")

        data = obtener_datos(simbolo)
        if data is None:
            continue

        data = calcular_indicadores(data)
        data = calcular_senales(data)
        historial_cruces(data)
        graficar(data, simbolo, axes[i])
        
        senal = calcular_senal(data)
        precio_actual = float(data['Close'].iloc[-1])

        cuenta = api.get_account()
        saldo = float(cuenta.cash)

        cantidad, stop_loss = validar_orden(precio_actual, saldo)

        print(f"Señal: {senal} | Precio: {precio_actual:.2f} | Cantidad: {cantidad} | Stop Loss: {stop_loss:.2f}")
        ejecutar_trade(simbolo, senal, cantidad)

    plt.tight_layout()
    plt.show()