"""
Módulo de gestión de riesgo. Calcula el tamaño de posición y el stop loss
basándose en el capital disponible y el precio actual.
"""
def validar_orden(precio_actual, saldo_cuenta):
    """
    Calcula la cantidad de acciones a comprar y el nivel de stop loss.

    Riesgo: 2% del capital. Stop loss: 3% por debajo del precio actual.
    Retorna (cantidad, stop_loss).
    """
    monto_a_invertir = saldo_cuenta * 0.02
    cantidad = int(monto_a_invertir // precio_actual)
    stop_loss = precio_actual * 0.97
    return cantidad, stop_loss
