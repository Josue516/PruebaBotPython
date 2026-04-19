"""
Módulo para la simulación de trading utilizando la API de Alpaca.
Este script calcula indicadores técnicos y ejecuta órdenes en la cuenta demo.
"""

import os
import yfinance as yf
import pandas as pd
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
import matplotlib.pyplot as plt


load_dotenv()
#CONFIGURACION DE LA API DE ALPACA
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')


# --- 1. DATOS ---
def obtener_datos():
    data = yf.download("AMZN", period="1y", interval="1d")

    # 🔥 Asegurar columnas simples
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # 🔍 Debug SIEMPRE (por ahora)
    print("Columnas:", data.columns)

    return data
    

# --- 2. INDICADORES ---
def calcular_indicadores(data):
    data['MA20'] = data['Close'].rolling(20).mean()
    data['MA50'] = data['Close'].rolling(50).mean()
    return data

def calcular_senales(data):
    data['Signal'] = 0
    data.loc[data['MA20'] > data['MA50'], 'Signal'] = 1
    data.loc[data['MA20'] < data['MA50'], 'Signal'] = -1
    data['Position'] = data['Signal'].diff()
    return data

#Grafico:
def graficar(data):
    plt.figure(figsize=(14, 7))

    # Precio y medias
    plt.plot(data['Close'], label='Precio de Cierre', alpha=0.5)
    plt.plot(data['MA20'], label='MA20')
    plt.plot(data['MA50'], label='MA50')

    # Señales
    data['Signal'] = 0
    data.loc[data['MA20'] > data['MA50'], 'Signal'] = 1
    data.loc[data['MA20'] < data['MA50'], 'Signal'] = -1
    data['Position'] = data['Signal'].diff()

    # Compra
    plt.plot(
        data[data['Position'] == 1].index,
        data['MA20'][data['Position'] == 1],
        '^',
        markersize=10,
        label='Compra'
    )

    # Venta
    plt.plot(
        data[data['Position'] == -1].index,
        data['MA20'][data['Position'] == -1],
        'v',
        markersize=10,
        label='Venta'
    )

    plt.title("Estrategia Cruce de Medias Móviles")
    plt.legend()
    plt.grid()
    plt.show()

# --- 3. SEÑAL ---
def generar_senal(data):
    ultima = data.iloc[-1]
    anterior = data.iloc[-2]

    ma20_ant = float(anterior['MA20'])
    ma50_ant = float(anterior['MA50'])
    ma20_ult = float(ultima['MA20'])
    ma50_ult = float(ultima['MA50'])

    if ma20_ant < ma50_ant and ma20_ult > ma50_ult:
        return "compra", "MA20 cruzó por encima de MA50"

    elif ma20_ant > ma50_ant and ma20_ult < ma50_ult:
        return "venta", "MA20 cruzó por debajo de MA50"

    return "nada", "No hay cruce entre MA20 y MA50"

# --- 4. EJECUCIÓN ---
def ejecutar_trade(senal):
    posiciones = api.list_positions()
    tengo_posicion = any(p.symbol == "AMZN" for p in posiciones)

    if senal == "compra" and not tengo_posicion:
        print("Ejecutando COMPRA...")
        api.submit_order(
            symbol="AMZN",
            qty=1,
            side="buy",
            type="market",
            time_in_force="gtc"
        )

    elif senal == "venta" and tengo_posicion:
        print("Ejecutando VENTA...")
        api.submit_order(
            symbol="AMZN",
            qty=1,
            side="sell",
            type="market",
            time_in_force="gtc"
        )

    elif senal == "compra" and tengo_posicion:
        print("No compra: ya tienes posición abierta")

    elif senal == "venta" and not tengo_posicion:
        print("No venta: no tienes posición")

    else:
        print("Sin acción")


# --- MAIN ---
data = obtener_datos()
data = calcular_indicadores(data)
graficar(data) #Generamos el grafico
senal, razon = generar_senal(data)

print(f"Señal detectada: {senal}")
print(f"Razón: {razon}")

ejecutar_trade(senal)