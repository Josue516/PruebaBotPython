# Gestor Patrimonial Automatizado

Bot de inversión automatizado desarrollado en Python. Analiza una lista de acciones predefinida, aplica filtros de calidad y ejecuta órdenes de compra y venta a través de la API de Alpaca en modo paper trading (sin dinero real).

---

## Que hace el bot

El bot sigue un ciclo de dos pasos cada vez que se ejecuta:

1. Revisa las posiciones abiertas y vende cualquier accion que haya caido mas del 15% desde el precio de compra (stop loss).
2. Escanea la watchlist en busca de nuevas oportunidades. Si una accion cumple los filtros de calidad y hay saldo disponible, ejecuta una orden de compra y registra la posicion en memoria.

---

## Estrategia de inversion

Para que el bot compre una accion, esta debe cumplir dos condiciones:

- Margen neto superior al 10% (empresa rentable).
- Precio actual por encima de su media movil de 200 dias (tendencia alcista).

El capital disponible se distribuye de forma equitativa entre todos los candidatos que pasen los filtros.

---

## Estructura del proyecto

```
trading_demo.py         Archivo principal. Orquesta todo el ciclo.
config.py               Parametros de la estrategia y lista de acciones.
modulos/
    scanner.py          Obtiene precios y aplica los filtros de calidad.
    engine.py           Logica de stop loss y calculo de cantidades.
    persistencia.py     Lee y escribe el portafolio en un archivo JSON.
data/
    portfolio.json      Memoria del bot. Guarda precios de compra y posiciones.
```

---

## Requisitos previos

- Python 3.9 o superior.
- Una cuenta gratuita en [Alpaca](https://alpaca.markets) para obtener las credenciales de la API.

---

## Instalacion

1. Clona el repositorio e instala las dependencias:

```bash
pip install -r requirements.txt
```

2. Crea un archivo `.env` en la raiz del proyecto con tus credenciales de Alpaca:

```env
ALPACA_API_KEY=tu_api_key
ALPACA_SECRET_KEY=tu_secret_key
```

---

## Uso

```bash
python trading_demo.py
```

El bot imprimira en consola cada decision que toma: que acciones mantiene, cuales vende por stop loss y cuales compra.

---

## Configuracion

Todos los parametros de la estrategia se encuentran en `config.py`. No es necesario modificar ningun otro archivo para ajustar el comportamiento del bot.

| Parametro            | Valor por defecto | Descripcion                                      |
|----------------------|-------------------|--------------------------------------------------|
| STOP_LOSS_THRESHOLD  | 0.15              | Vende si la accion cae mas del 15%               |
| MIN_NET_MARGIN       | 0.10              | Solo compra empresas con margen neto mayor al 10% |
| MIN_CASH_FOR_BUY     | 100.0             | Saldo minimo para buscar nuevas compras           |

La lista de acciones monitoreadas (WATCHLIST) tambien se define en `config.py`.

---

## Modo simulacion

En `trading_demo.py` existe la variable `MODO_SIMULACION`. Si se establece en `True`, el bot analiza y muestra las decisiones en consola pero no envia ninguna orden real a Alpaca. Util para probar cambios en la estrategia.

```python
MODO_SIMULACION = True  # No ejecuta ordenes reales
```

---

## Tecnologias utilizadas

- Python
- yfinance
- pandas
- alpaca-trade-api
- python-dotenv
- matplotlib
