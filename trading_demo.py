"""
Módulo principal del Gestor Patrimonial Automatizado.

Este script orquesta el ciclo completo de gestión de inversiones:
1. Revisa las posiciones actuales y aplica stop loss si es necesario.
2. Escanea la watchlist en busca de nuevas oportunidades de compra.
3. Distribuye el capital disponible entre los candidatos aptos.
4. Ejecuta las órdenes en la API de Alpaca y actualiza la memoria local.
"""

import os
from datetime import datetime

import alpaca_trade_api as tradeapi
from dotenv import load_dotenv

from config import WATCHLIST, API_CONFIG
from modulos.persistencia import cargar_portafolio, actualizar_posicion
from modulos.scanner import cumple_filtros_calidad, obtener_precio_actual
from modulos.engine import calcular_salida, calcular_cantidad_compra, procesar_dividendos_y_efectivo

# Si es True, el bot analiza pero NO envía órdenes reales a Alpaca.
MODO_SIMULACION = False

load_dotenv()


def _revisar_stop_loss(api, portafolio):
    """
    Recorre las posiciones abiertas y vende aquellas que hayan caído
    por debajo del umbral de stop loss definido en config.py.

    Args:
        api: Instancia autenticada de la API de Alpaca.
        portafolio (dict): Estado actual del portafolio cargado desde memoria.
    """
    print("\n[1] Revisando Stop Loss para posiciones actuales...")
    simbolos_en_cartera = list(portafolio["positions"].keys())

    for simbolo in simbolos_en_cartera:
        info = portafolio["positions"][simbolo]
        precio_actual = obtener_precio_actual(simbolo)

        if precio_actual:
            debe_vender, variacion = calcular_salida(precio_actual, info["buy_price"])

            if debe_vender:
                print(f"ALERTA STOP LOSS: {simbolo} ha caído {variacion:.2%}. Ejecutando venta.")
                if not MODO_SIMULACION:
                    api.submit_order(
                        symbol=simbolo,
                        qty=info["shares"],
                        side="sell",
                        type="market"
                    )
                    actualizar_posicion(simbolo, 0, 0, añadir=False)
            else:
                print(f"{simbolo}: Rendimiento actual {variacion:+.2%}. Manteniendo.")
        else:
            print(f"No se pudo obtener el precio para {simbolo}. Saltando...")


def _buscar_oportunidades(api, portafolio):
    """
    Escanea la watchlist, filtra candidatos aptos y distribuye el capital
    disponible entre ellos para ejecutar compras.

    Args:
        api: Instancia autenticada de la API de Alpaca.
        portafolio (dict): Estado actual del portafolio cargado desde memoria.
    """
    print("\n[2] Escaneando Watchlist para nuevas oportunidades...")
    cuenta = api.get_account()
    hay_efectivo, saldo_total = procesar_dividendos_y_efectivo(cuenta)

    if not hay_efectivo:
        print(f"Saldo insuficiente (${saldo_total:.2f}). Esperando dividendos o depósitos.")
        return

    # Filtrar símbolos que no están en cartera y cumplen los criterios de calidad
    candidatos_aptos = [
        simbolo for simbolo in WATCHLIST
        if simbolo not in portafolio["positions"] and cumple_filtros_calidad(simbolo)
    ]

    if not candidatos_aptos:
        print("No se encontraron nuevas oportunidades que cumplan los filtros.")
        return

    # Distribuir el saldo equitativamente entre los candidatos
    capital_por_accion = saldo_total / len(candidatos_aptos)
    print(f"\nSaldo total: ${saldo_total:.2f} | Distribución: ${capital_por_accion:.2f} por acción.")

    for simbolo in candidatos_aptos:
        precio_compra = obtener_precio_actual(simbolo)
        if not precio_compra:
            continue

        cantidad = calcular_cantidad_compra(capital_por_accion, precio_compra)

        if cantidad > 0:
            print(f"EJECUTANDO COMPRA: {simbolo} | Cantidad: {cantidad} | Precio: ${precio_compra:.2f}")
            if not MODO_SIMULACION:
                # Enviar orden de compra a Alpaca
                api.submit_order(
                    symbol=simbolo,
                    qty=cantidad,
                    side="buy",
                    type="market",
                    time_in_force="gtc"
                )
                # Registrar la compra en memoria local para el stop loss futuro
                actualizar_posicion(simbolo, precio_compra, cantidad)
                print(f"{simbolo} registrado en portfolio.json a ${precio_compra:.2f}")
        else:
            print(f"{simbolo}: Capital insuficiente para comprar al menos 1 acción.")


def ejecutar_gestor():
    """
    Función principal que ejecuta el ciclo completo del gestor patrimonial.

    Inicializa la conexión con Alpaca, carga el portafolio en memoria,
    revisa el stop loss de posiciones abiertas y busca nuevas oportunidades
    de compra en la watchlist.
    """
    print(f"--- Iniciando sesión del Gestor Patrimonial ({datetime.now().strftime('%Y-%m-%d')}) ---")

    # Inicializar conexión con la API de Alpaca usando credenciales del .env
    api = tradeapi.REST(
        os.getenv("ALPACA_API_KEY"),
        os.getenv("ALPACA_SECRET_KEY"),
        API_CONFIG["BASE_URL"]
    )

    # Cargar el estado del portafolio desde el archivo JSON local
    portafolio = cargar_portafolio()

    _revisar_stop_loss(api, portafolio)
    _buscar_oportunidades(api, portafolio)

    print("\n--- Ejecución finalizada con éxito ---")


if __name__ == "__main__":
    ejecutar_gestor()
