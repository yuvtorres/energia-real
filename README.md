# energia-real

__Plataforma para análisis y pronóstico de la generación de energía en España__

---

## Estructura

Esta aplicación se estructura en tres partes principales:

- Gestión de datos: bases de datos y herramientas de gestión (ETL).

- Análisis de los datos y predicción: API para realizar el análisis de datos y el pronóstico.

- Visualización de datos y resultados: interfaz WEB de visualización.

## Gestión de datos

La gestión de datos se realiza a través de un programa de línea de comandos que interactua con las fuentes de datos, trayendo los datos y organizandolos en las diferentes bases de datos. Las fuentes de datos son:

- ![REE](https://www.ree.es/): Empresa encargada de la operación de la red de transmisión (ETSO). 
- ![AEMET](http://www.aemet.es/): Agencia estatal de meteorología.

Las bases de datos que se tendrán son:

- Influx: para datos temporales reales, como medidas de generación o precios ofertados.

- MySQL: para los datos de pronóstico, o datos estructurados.

- MongoDB: para los demás datos.

## Análisis de datos y predicción

Esta API realiza el análisis de los datos y la predicción a partir de la información dada por el módulo anterior. 
Así mismo los parámetros de los modelos de predicción son ajustados automáticamente cada cierto tiempo incluyendo la nueva información.

## Visualialización

La visualización se hace a través de una WEB que conecta a la API de análisis de datos para extraer los resultados.


