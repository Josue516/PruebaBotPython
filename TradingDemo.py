import yfinance as yf
import pandas as pd
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
import os

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


# --- 3. SEÑAL ---
def generar_senal(data):
    data = data.dropna()

    ultima = data.iloc[-1]
    anterior = data.iloc[-2]

    ma20_ant = float(anterior['MA20'])
    ma50_ant = float(anterior['MA50'])
    ma20_ult = float(ultima['MA20'])
    ma50_ult = float(ultima['MA50'])

    if ma20_ant < ma50_ant and ma20_ult > ma50_ult:
        return "compra"

    elif ma20_ant > ma50_ant and ma20_ult < ma50_ult:
        return "venta"

    return "nada"


# --- 4. EJECUCIÓN ---
def ejecutar_trade(senal):
    posiciones = api.list_positions()
    tengo_posicion = any(p.symbol == "AMZN" for p in posiciones)

    if senal == "compra" and not tengo_posicion:
        print("Comprando...")
        api.submit_order(
            symbol="AMZN",
            qty=1,
            side="buy",
            type="market",
            time_in_force="gtc"
        )

    elif senal == "venta" and tengo_posicion:
        print("Vendiendo...")
        api.submit_order(
            symbol="AMZN",
            qty=1,
            side="sell",
            type="market",
            time_in_force="gtc"
        )
    else:
        print("Sin acción")


# --- MAIN ---
data = obtener_datos()
data = calcular_indicadores(data)
senal = generar_senal(data)

print(f"Señal detectada: {senal}")
ejecutar_trade(senal)