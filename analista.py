"""
Módulo de análisis técnico. Calcula indicadores y genera señales de trading
basadas en el cruce de medias móviles (MA20 y MA50).
"""
def calcular_indicadores(data):
    """Agrega las columnas MA20 y MA50 al DataFrame."""
    data['MA20'] = data['Close'].rolling(20).mean()
    data['MA50'] = data['Close'].rolling(50).mean()
    return data
def historial_cruces(data):
    cruces = data[data['Position'] != 0]

    if not cruces.empty:
        print("Historial de cruces detectados:")
        print(cruces[['Close', 'MA20', 'MA50', 'Position']])
    else:
        print("No se detectó ningún cruce en el periodo.")

def calcular_senales(data):
    data['Signal'] = 0
    data.loc[data['MA20'] > data['MA50'], 'Signal'] = 1
    data.loc[data['MA20'] < data['MA50'], 'Signal'] = -1
    data['Position'] = data['Signal'].diff()
    return data

def calcular_senal(data):
    """Usa la última posición para decidir acción."""
    ultima = data['Position'].iloc[-1]

    if ultima == 1:
        return 1
    elif ultima == -1:
        return -1
    return 0


