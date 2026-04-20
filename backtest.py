import pandas as pd
from trading_demo import obtener_datos
from analista import calcular_indicadores, calcular_senales, calcular_senal

def ejecutar_comparativa(simbolo, capital_inicial=1000):
    data = obtener_datos(simbolo)
    
    if data is None or data.empty or len(data) < 50:
        return None

    # --- ESTRATEGIA 1: EL BOT ---
    data_bot = calcular_indicadores(data.copy())
    data_bot = calcular_senales(data_bot)
    
    saldo_bot = capital_inicial
    posicion_bot = 0
    
    for i in range(50, len(data_bot)):
        ventana = data_bot.iloc[:i+1]
        precio_cierre = float(ventana['Close'].iloc[-1])
        senal = calcular_senal(ventana)

        if senal == 1 and posicion_bot == 0:
            posicion_bot = saldo_bot // precio_cierre
            saldo_bot -= posicion_bot * precio_cierre
        elif senal == -1 and posicion_bot > 0:
            saldo_bot += posicion_bot * precio_cierre
            posicion_bot = 0

    final_bot = saldo_bot + (posicion_bot * data_bot['Close'].iloc[-1])

    # --- ESTRATEGIA 2: BUY & HOLD (Comprar y Mantener) ---
    # Compramos el primer día que tengamos datos (fila 0)
    precio_inicio = float(data['Close'].iloc[0])
    precio_fin = float(data['Close'].iloc[-1])
    
    acciones_hold = capital_inicial // precio_inicio
    efectivo_sobrante = capital_inicial % precio_inicio
    final_hold = efectivo_sobrante + (acciones_hold * precio_fin)

    rend_bot = ((final_bot - capital_inicial) / capital_inicial) * 100
    rend_hold = ((final_hold - capital_inicial) / capital_inicial) * 100

    return {
        "Símbolo": simbolo,
        "Final Bot": round(final_bot, 2),
        "Rend Bot %": round(rend_bot, 2),
        "Final Hold": round(final_hold, 2),
        "Rend Hold %": round(rend_hold, 2),
        "Diferencia": round(rend_bot - rend_hold, 2)
    }

if __name__ == "__main__":
    simbolos = ["INTC", "AAPL", "MSFT", "NVDA"] # Añadí NVDA para comparar
    resultados = []
    
    for s in simbolos:
        res = ejecutar_comparativa(s)
        if res:
            resultados.append(res)
    
    df = pd.DataFrame(resultados)
    print("\n--- BATALLA FINAL: BOT VS HOLD ---")
    print(df.to_string(index=False))