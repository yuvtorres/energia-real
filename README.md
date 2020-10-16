# energia-real

__API para análisis y pronóstico de la generación de energía en España__

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

Adicionalmente otro tipo de datos como: lista de municipios, lista de estaciones meteriologicas, etc. Se almacenan en una base de datos de mongodb.

## Análisis de datos

La aplicación tendrá una interfaz de terminal para manejar las bases de datos, importar medidas y hacer análisis gruesos del contenito de las bases de datos.

Adicionalmente como interfaz se tiene una web que interactúa con la API-WEB, cuyos endpoints tendrán el pronóstico de consumo de las próximas 24 horas de generación renovables (eólica y fotovoltáica).

## Visualización

El gestor es un programa de terminal que importa los datos desde REE y AEMET, y permite ver un resumen general de estos.

## El Pronóstico
