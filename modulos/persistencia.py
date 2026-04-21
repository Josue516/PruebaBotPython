"""
Módulo de persistencia del portafolio.

Gestiona la lectura y escritura del estado del portafolio en un archivo JSON local.
Esto permite que el bot recuerde a qué precio compró cada acción entre ejecuciones,
lo cual es esencial para calcular el stop loss correctamente al día siguiente.
"""

import json
import os

from config import PORTFOLIO_FILE


def cargar_portafolio():
    """
    Carga el portafolio desde el archivo JSON local.

    Si el archivo no existe, lo crea con una estructura vacía por defecto.
    También valida que las claves esenciales estén presentes para evitar
    errores en tiempo de ejecución.

    Returns:
        dict: Portafolio con las claves 'cash_available' y 'positions'.
    """
    estandar = {"cash_available": 0.0, "positions": {}}

    if not os.path.exists(PORTFOLIO_FILE):
        guardar_portafolio(estandar)
        return estandar

    try:
        with open(PORTFOLIO_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Garantizar que las claves mínimas existan aunque el archivo esté incompleto
            if "positions" not in data:
                data["positions"] = {}
            if "cash_available" not in data:
                data["cash_available"] = 0.0
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        # Si el archivo está corrupto o no se puede leer, retornar estructura vacía
        return estandar


def guardar_portafolio(datos):
    """
    Guarda el estado actual del portafolio en el archivo JSON.

    Crea el directorio de datos si no existe.

    Args:
        datos (dict): Diccionario con el estado completo del portafolio.
    """
    os.makedirs(os.path.dirname(PORTFOLIO_FILE), exist_ok=True)
    with open(PORTFOLIO_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4)


def actualizar_posicion(simbolo, precio_compra, cantidad, añadir=True):
    """
    Registra o elimina una posición en la memoria del portafolio.

    Args:
        simbolo (str): Ticker de la acción (ej: "AAPL").
        precio_compra (float): Precio al que se ejecutó la compra.
        cantidad (int): Número de acciones compradas.
        añadir (bool): Si es True, registra la posición. Si es False, la elimina.
            Por defecto True.
    """
    portafolio = cargar_portafolio()

    if añadir:
        # Guardar precio de compra y cantidad para el cálculo futuro de stop loss
        portafolio["positions"][simbolo] = {
            "buy_price": precio_compra,
            "shares": cantidad,
            "last_tick": precio_compra
        }
    else:
        # Eliminar la posición tras una venta
        if simbolo in portafolio["positions"]:
            del portafolio["positions"][simbolo]

    guardar_portafolio(portafolio)
