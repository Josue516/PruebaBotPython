"""
Módulo principal de la simulación de trading con la API de Alpaca.
Orquesta la descarga de datos, análisis técnico, gestión de riesgo y ejecución de órdenes.
"""
import os
import alpaca_trade_api as tradeapi
from datetime import datetime
from dotenv import load_dotenv
from config import STRATEGY, WATCHLIST, PORTFOLIO_FILE, API_CONFIG
from modulos.persistencia import cargar_portafolio, guardar_portafolio, actualizar_posicion
from modulos.scanner import cumple_filtros_calidad, obtener_precio_actual
from modulos.engine import calcular_salida, calcular_cantidad_compra, procesar_dividendos_y_efectivo

# --- CONFIGURACIÓN DE PRUEBA ---
MODO_SIMULACION = True # Cambia a False para ejecutar órdenes reales en Alpaca
load_dotenv()
def ejecutar_gestor():
    print(f"--- Iniciando sesión del Gestor Patrimonial ({datetime.now().strftime('%Y-%m-%d')}) ---")
    # 1. Inicializar API y Cargar Memoria
    api = tradeapi.REST(
        os.getenv("ALPACA_API_KEY"), 
        os.getenv("ALPACA_SECRET_KEY"), 
        API_CONFIG["BASE_URL"]
    )
    portafolio = cargar_portafolio()
    
    # 2. REVISIÓN DE CARTERA (Protección del Capital - Stop Loss)
    print("\n[1] Revisando Stop Loss para posiciones actuales...")
    # Creamos una lista de llaves para evitar errores al modificar el dict durante el loop
    simbolos_en_cartera = list(portafolio["positions"].keys())
    
    for simbolo in simbolos_en_cartera:
        info = portafolio["positions"][simbolo]
        precio_actual = obtener_precio_actual(simbolo)
        
        if precio_actual:
            debe_vender, variacion = calcular_salida(precio_actual, info["buy_price"])
            
            if debe_vender:
                print(f"ALERTA STOP LOSS: {simbolo} ha caído {variacion:.2%}. Ejecutando venta.")
                if not MODO_SIMULACION:
                    api.submit_order(symbol=simbolo, qty=info["shares"], side="sell", type="market")
                    actualizar_posicion(simbolo, 0, 0, añadir=False)
            else:
                print(f"{simbolo}: Rendimiento actual {variacion:+.2%}. Manteniendo.")
        else:
            print(f"No se pudo obtener el precio para {simbolo}. Saltando...")

# 3. BÚSQUEDA DE OPORTUNIDADES (Stock Screening & Diversificación)
    print("\n[2] Escaneando Watchlist para nuevas oportunidades...")
    cuenta = api.get_account()
    hay_efectivo, saldo_total = procesar_dividendos_y_efectivo(cuenta)
    
    if hay_efectivo:
        # PASO A: Filtrar quiénes son aptos
        candidatos_aptos = []
        for simbolo in WATCHLIST:
            if simbolo not in portafolio["positions"]:
                if cumple_filtros_calidad(simbolo):
                    candidatos_aptos.append(simbolo)
                else:
                    print(f"{simbolo} no cumple los filtros de calidad/momentum hoy.")

        # PASO B: Si hay candidatos, repartir el saldo y comprar
        if candidatos_aptos:
            num_candidatos = len(candidatos_aptos)
            capital_por_accion = saldo_total / num_candidatos
            
            print(f"\n Saldo total: ${saldo_total:.2f} | Distribución: ${capital_por_accion:.2f} por acción.")

            for simbolo in candidatos_aptos:
                precio_compra = obtener_precio_actual(simbolo)
                if precio_compra:
                    cantidad = calcular_cantidad_compra(capital_por_accion, precio_compra)
                    
                    if cantidad > 0:
                        print(f" COMPRA PROGRAMADA: {simbolo} | Cantidad: {cantidad} | Total: ${cantidad * precio_compra:.2f}")
                        if not MODO_SIMULACION:
                            api.submit_order(symbol=simbolo, qty=cantidad, side="buy", type="market")
                            actualizar_posicion(simbolo, precio_compra, cantidad)
                    else:
                        print(f"{simbolo}: Capital insuficiente para comprar al menos 1 acción.")
        else:
            print("🔍 No se encontraron nuevas oportunidades que cumplan los filtros.")
    else:
        print(f"Saldo insuficiente (${saldo_total:.2f}). Esperando dividendos o depósitos.")

    print("\n--- Ejecución finalizada con éxito ---")

if __name__ == "__main__":
    ejecutar_gestor()