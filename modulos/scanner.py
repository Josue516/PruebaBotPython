import yfinance as yf
from config import STRATEGY

def obtener_precio_actual(simbolo):
    """
    Obtiene el último precio de cierre disponible para un símbolo.
    Útil para la revisión de Stop Loss sin importar si está en la Watchlist.
    """
    try:
        ticker = yf.Ticker(simbolo)
        # Usamos period="1d" para obtener el dato más reciente de forma rápida
        data = ticker.history(period="1d")
        if not data.empty:
            return float(data['Close'].iloc[-1])
        return None
    except Exception as e:
        print(f"Error obteniendo precio para {simbolo}: {e}")
        return None

def cumple_filtros_calidad(simbolo):
    """
    Verifica si una acción es apta para la estrategia:
    1. Margen Neto > 10%
    2. Precio > Media Móvil 200 días
    """
    try:
        ticker = yf.Ticker(simbolo)
        # 1. Obtener fundamentales
        info = ticker.info
        margen_neto = info.get('profitMargins', 0)
        
        # 2. Obtener datos históricos para SMA 200
        hist = ticker.history(period="1y")
        if len(hist) < 200:
            return False
            
        sma_200 = hist['Close'].rolling(window=200).mean().iloc[-1]
        precio_actual = hist['Close'].iloc[-1]

        # Validación de reglas
        tiene_salud = margen_neto > STRATEGY["MIN_NET_MARGIN"]
        tiene_momentum = precio_actual > sma_200

        print(f"[{simbolo}] Margen: {margen_neto:.2%}, SMA 200: {sma_200:.2f}, Actual: {precio_actual:.2f}")

        return tiene_salud and tiene_momentum

    except Exception as e:
        print(f"Error analizando {simbolo}: {e}")
        return False

