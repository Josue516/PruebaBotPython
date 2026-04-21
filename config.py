"""
Archivo de configuración central del Gestor Patrimonial.

Define todas las reglas de inversión, la lista de vigilancia (watchlist)
y los parámetros técnicos de la API. Modificar este archivo es suficiente
para ajustar el comportamiento del bot sin tocar la lógica principal.
"""

# --- Configuración de Archivos ---
DATA_DIR = "data"
PORTFOLIO_FILE = f"{DATA_DIR}/portfolio.json"  # Ruta del archivo de memoria del portafolio

# --- Reglas de Inversión (Filosofía Gestor Patrimonial) ---
STRATEGY = {
    "STOP_LOSS_THRESHOLD": 0.15,   # Vender si la acción cae más del 15% desde la compra
    "MIN_NET_MARGIN": 0.10,        # Solo comprar empresas con margen neto superior al 10%
    "SMA_LONG_PERIOD": 200,        # Periodo de la media móvil de largo plazo
    "REINVEST_DIVIDENDS": True,    # Activar reinversión automática del efectivo disponible
    "MIN_CASH_FOR_BUY": 100.0      # Saldo mínimo en cuenta para iniciar búsqueda de compras
}

# --- Lista de Vigilancia (Stock Screening) ---
# Acciones de calidad que el bot monitoreará para posibles compras.
# Solo se comprarán si cumplen los filtros de calidad definidos en scanner.py.
WATCHLIST = [
    "AAPL", "MSFT", "GOOGL", "NVDA", "TSLA",
    "AMZN", "META", "BRK-B", "V", "JNJ"
]

# --- Configuración Técnica de la API ---
API_CONFIG = {
    "BASE_URL": "https://paper-api.alpaca.markets",  # Cambiar a URL live para dinero real
    "YF_PERIOD": "2y",    # Periodo de descarga de datos (mínimo 1 año para SMA 200)
    "YF_INTERVAL": "1d"   # Intervalo diario, suficiente para esta estrategia
}
