"""Implementa la estrategia de STOP LOSS definida en el archivo config.py"""
from config import STRATEGY

def calcular_salida(precio_actual, precio_compra):
    """
    Evalúa si se debe salir de una posición basado en el Stop Loss del 15%.
    """
    # Calculamos la variación porcentual (ej: -0.15 para un 15% de caída)
    variacion = (precio_actual - precio_compra) / precio_compra
    
    # Si la variación es menor o igual al umbral negativo (ej: -0.15)
    if variacion <= -STRATEGY["STOP_LOSS_THRESHOLD"]:
        return True, variacion
    
    return False, variacion

def calcular_cantidad_compra(saldo_disponible, precio_accion):
    """
    Determina cuántas acciones comprar basándose en el efectivo.
    Aplica una lógica simple de usar todo el saldo para maximizar el interés compuesto.
    """
    if saldo_disponible < precio_accion:
        return 0
    
    cantidad = int(saldo_disponible // precio_accion)
    return cantidad

def procesar_dividendos_y_efectivo(cuenta_alpaca):
    """
    Detecta si hay saldo 'extra' para reinvertir.
    """
    efectivo = float(cuenta_alpaca.cash)
    return efectivo >= STRATEGY["MIN_CASH_FOR_BUY"], efectivo