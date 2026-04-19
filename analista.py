"""
Módulo de análisis técnico. Calcula indicadores y genera señales de trading
basadas en el cruce de medias móviles (MA20 y MA50).
"""
def calcular_indicadores(data):
    """Agrega las columnas MA20 y MA50 al DataFrame."""
    data['MA20'] = data['Close'].rolling(20).mean()
    data['MA50'] = data['Close'].rolling(50).mean()
    return data
def calcular_senal(data):
    """Detecta cruce de medias y retorna 1 (compra), -1 (venta) o 0 (sin señal)."""
    ma20_ult = data['MA20'].iloc[-1]
    ma50_ult = data['MA50'].iloc[-1]
    ma20_ant = data['MA20'].iloc[-2]
    ma50_ant = data['MA50'].iloc[-2]

    if ma20_ant <= ma50_ant and ma20_ult > ma50_ult:
        return 1
    if ma20_ant >= ma50_ant and ma20_ult < ma50_ult:
        return -1
    return 0
