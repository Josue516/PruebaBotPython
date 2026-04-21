"""Este bot se encarga de guardar y leer los datos para que el bot no olvide a que precio compro las acciones"""
import json
import os
from config import PORTFOLIO_FILE

def cargar_portafolio():
    """Carga el estado del portafolio manejando archivos vacíos o corruptos."""
    if not os.path.exists(PORTFOLIO_FILE):
        inicial = {"cash_available": 0.0, "positions": {}}
        guardar_portafolio(inicial)
        return inicial
    
    try:
        with open(PORTFOLIO_FILE, 'r') as f:
            content = f.read().strip()
            if not content:  # Si el archivo está vacío (0 bytes)
                return {"cash_available": 0.0, "positions": {}}
            return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ Error: El archivo JSON está corrupto. Creando uno nuevo.")
        return {"cash_available": 0.0, "positions": {}}

def guardar_portafolio(datos):
    """Guarda el estado actual en el JSON."""
    os.makedirs(os.path.dirname(PORTFOLIO_FILE), exist_ok=True)
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(datos, f, indent=4)

def actualizar_posicion(simbolo, precio_compra, cantidad, añadir=True):
    """Registra o elimina una posición en la memoria."""
    portafolio = cargar_portafolio()
    if añadir:
        portafolio["positions"][simbolo] = {
            "buy_price": precio_compra,
            "shares": cantidad,
            "last_tick": precio_compra
        }
    else:
        if simbolo in portafolio["positions"]:
            del portafolio["positions"][simbolo]
    
    guardar_portafolio(portafolio)