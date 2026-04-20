"""Archivo para controlar el tiempo de bucle de trading_demo"""
import time
import schedule
from trading_demo import ejecutar_bot_completo

def tarea_programada():
    print(f"\n[{time.strftime('%H:%M:%S')}] Iniciando ciclo de trading...")
    try:
        ejecutar_bot_completo()
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# --- CONFIGURACIÓN DEL TIEMPO ---
# Para probar rápido, cada 5 minutos
minutos_intervalo = 5
schedule.every(minutos_intervalo).minutes.do(tarea_programada)

if __name__ == "__main__":
    print(f"Bot en marcha. Se ejecutará cada {minutos_intervalo} minutos.")
    # Ejecutamos una vez al inicio para no esperar los primeros 5 min
    tarea_programada() 
    
    while True:
        schedule.run_pending()
        time.sleep(1)