# Trading Bot con Python 

Este proyecto es un bot de trading básico desarrollado en Python que utiliza una estrategia de cruce de medias móviles para tomar decisiones de compra y venta de forma automatizada.

Actualmente funciona con una cuenta de **paper trading (simulación)**, por lo que no utiliza dinero real.

---

## Características

* Descarga de datos financieros con `yfinance`
* Cálculo de indicadores técnicos (Media Móvil 20 y 50)
* Generación de señales de trading (compra / venta / nada)
* Integración con API de Alpaca
* Ejecución automática de órdenes en cuenta demo
* Validación de posición para evitar operaciones repetidas

---

## Estrategia utilizada

**Cruce de Medias Móviles:**

* Cuando la MA20 cruza por encima de la MA50 → **Compra**
* Cuando la MA20 cruza por debajo de la MA50 → **Venta**
* En cualquier otro caso → **No hacer nada**

---

## Configuración de variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
ALPACA_API_KEY=tu_api_key
ALPACA_SECRET_KEY=tu_secret_key
```


---

## ▶️ Uso

Ejecuta el bot:

```bash
python trading_demo.py
```

---

## Ejemplo de flujo

1. Obtiene datos recientes del mercado
2. Calcula indicadores técnicos
3. Detecta señales
4. Verifica si ya hay posición abierta
5. Ejecuta orden si corresponde

---

## Tecnologías utilizadas

* Python
* Pandas
* yfinance
* Alpaca API

---

## Próximas mejoras

* [ ] Loop automático (ejecución continua)
* [ ] Stop Loss / Take Profit
* [ ] Backtesting avanzado
* [ ] Múltiples activos
* [ ] Integración con IA

---

## Nota final

Este es un proyecto en evolución.
La idea es ir escalando desde un bot simple hasta un sistema más avanzado.

Espero no olvidarme de este proyecto.

