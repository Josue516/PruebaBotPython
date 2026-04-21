"""
Módulo de escaneo y filtrado de acciones (Stock Screening).

Proporciona funciones para obtener precios en tiempo real y evaluar
si una acción cumple los criterios de calidad definidos en la estrategia:
margen neto mínimo y precio por encima de la media móvil de 200 días.
"""

import yfinance as yf
from config import STRATEGY


def obtener_precio_actual(simbolo):
    """
    Obtiene el último precio de cierre disponible para un símbolo.

    Se usa tanto para la revisión de stop loss como para calcular
    el precio de compra antes de enviar una orden.

    Args:
        simbolo (str): Ticker de la acción (ej: "AAPL").

    Returns:
        float: Último precio de cierre, o None si ocurre un error.
    """
    try:
        ticker = yf.Ticker(simbolo)
        data = ticker.history(period="1d")
        if not data.empty:
            return float(data['Close'].iloc[-1])
        return None
    except (ValueError, KeyError) as e:
        print(f"Error obteniendo precio para {simbolo}: {e}")
        return None


def cumple_filtros_calidad(simbolo):
    """
    Verifica si una acción es apta para la estrategia de inversión.

    Aplica dos filtros:
    1. Margen neto superior al mínimo definido en config.py (por defecto 10%).
    2. Precio actual por encima de la media móvil de 200 días (momentum alcista).

    Args:
        simbolo (str): Ticker de la acción (ej: "MSFT").

    Returns:
        bool: True si cumple ambos filtros, False en caso contrario.
    """
    try:
        ticker = yf.Ticker(simbolo)

        # Obtener fundamentales: margen neto de los últimos 12 meses
        info = ticker.info
        margen_neto = info.get('profitMargins', 0)

        # Obtener histórico para calcular la SMA de 200 días
        hist = ticker.history(period="1y")
        if len(hist) < 200:
            # No hay suficiente historial para calcular la SMA 200
            return False

        sma_200 = hist['Close'].rolling(window=200).mean().iloc[-1]
        precio_actual = hist['Close'].iloc[-1]

        # Evaluar ambas condiciones de la estrategia
        tiene_salud = margen_neto > STRATEGY["MIN_NET_MARGIN"]
        tiene_momentum = precio_actual > sma_200

        print(
            f"[{simbolo}] Margen: {margen_neto:.2%} | "
            f"SMA 200: {sma_200:.2f} | Actual: {precio_actual:.2f}"
        )

        return tiene_salud and tiene_momentum

    except (ValueError, KeyError) as e:
        print(f"Error analizando {simbolo}: {e}")
        return False
