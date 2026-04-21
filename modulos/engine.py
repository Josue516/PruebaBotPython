"""
Módulo de lógica de negocio de la estrategia de inversión.

Contiene las funciones que implementan las reglas de decisión del bot:
cuándo salir de una posición (stop loss), cuántas acciones comprar
y si hay efectivo disponible para reinvertir.
"""

from config import STRATEGY


def calcular_salida(precio_actual, precio_compra):
    """
    Evalúa si se debe cerrar una posición por stop loss.

    Compara la variación porcentual entre el precio de compra y el actual
    contra el umbral definido en config.py (por defecto -15%).

    Args:
        precio_actual (float): Precio de mercado actual de la acción.
        precio_compra (float): Precio al que se compró originalmente.

    Returns:
        tuple: (debe_vender: bool, variacion: float)
            - debe_vender: True si la caída supera el umbral de stop loss.
            - variacion: Variación porcentual (negativa si hay pérdida).
    """
    # Variación porcentual respecto al precio de compra (ej: -0.15 = caída del 15%)
    variacion = (precio_actual - precio_compra) / precio_compra

    if variacion <= -STRATEGY["STOP_LOSS_THRESHOLD"]:
        return True, variacion

    return False, variacion


def calcular_cantidad_compra(saldo_disponible, precio_accion):
    """
    Determina cuántas acciones enteras se pueden comprar con el saldo asignado.

    Usa división entera para no comprar fracciones de acciones.
    Retorna 0 si el saldo es insuficiente para comprar al menos una acción.

    Args:
        saldo_disponible (float): Capital asignado para este símbolo.
        precio_accion (float): Precio actual de la acción.

    Returns:
        int: Número de acciones a comprar (0 si no alcanza).
    """
    if saldo_disponible < precio_accion:
        return 0

    return int(saldo_disponible // precio_accion)


def procesar_dividendos_y_efectivo(cuenta_alpaca):
    """
    Verifica si hay suficiente efectivo en la cuenta para buscar nuevas compras.

    Compara el saldo en efectivo contra el mínimo requerido definido
    en config.py (por defecto $100).

    Args:
        cuenta_alpaca: Objeto de cuenta retornado por la API de Alpaca.

    Returns:
        tuple: (hay_efectivo: bool, saldo: float)
            - hay_efectivo: True si el saldo supera el mínimo para comprar.
            - saldo: Monto exacto de efectivo disponible en la cuenta.
    """
    efectivo = float(cuenta_alpaca.cash)
    return efectivo >= STRATEGY["MIN_CASH_FOR_BUY"], efectivo
