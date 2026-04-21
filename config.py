"""Archivo con las reglas que el bot seguira para comprar y vender acciones"""
# --- Configuración de Archivos ---
DATA_DIR = "data"
PORTFOLIO_FILE = f"{DATA_DIR}/portfolio.json"

# --- Reglas de Inversión (Filosofía Gestor Patrimonial) ---
STRATEGY = {
    "STOP_LOSS_THRESHOLD": 0.15,      # 15% de caída máxima
    "MIN_NET_MARGIN": 0.10,           # Margen neto > 10%
    "SMA_LONG_PERIOD": 200,           # Media móvil de largo plazo
    "REINVEST_DIVIDENDS": True,       # Activa la lógica de reinversión
    "MIN_CASH_FOR_BUY": 100.0         # Mínimo de efectivo para buscar nuevas compras
}

# --- Lista de Vigilancia (Stock Screening) ---
# Aquí pones las acciones de calidad que quieres que el bot monitoree
WATCHLIST = [
    "AAPL", "MSFT", "GOOGL", "NVDA", "TSLA", 
    "AMZN", "META", "BRK-B", "V", "JNJ"
]

# --- Configuración Técnica ---
API_CONFIG = {
    "BASE_URL": "https://paper-api.alpaca.markets", # Cambiar a 'live' para dinero real
    "YF_PERIOD": "2y",   # Necesitamos al menos 1 año para la SMA 200
    "YF_INTERVAL": "1d"  # Datos diarios son suficientes para este enfoque
}