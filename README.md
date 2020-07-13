# energia-real

API para ver la generación real instantanea por tipo de tecnología, y un pronóstico para las próximas 24 horas de la generación renovable.

---
## Datos

- ![REE](https://www.ree.es/): Empresa encargada de la operación de la red de transmisión (ETSO). 
- ![AEMET](http://www.aemet.es/): Agencia estatal de meteorología.

Por tratarse de datos temporales, se manejarán en Influx, una base de datos orientada a las series temporales.

Adicionalmente otro tipo de datos como: lista de municipios, lista de estaciones meteriologicas, etc. Se almacenan en una base de datos de mongodb.

# La Aplicación

La aplicación tendrá una interfaz de terminal para manejar las bases de datos, importar medidas y hacer análisis gruesos del contenito de las bases de datos.

Adicionalmente como interfaz se tiene una web que interactúa con la API-WEB, cuyos endpoints tendrán el pronóstico de consumo de las próximas 24 horas de generación renovables (eólica y fotovoltáica).

## El gestor

El gestor es un programa de terminal que importa los datos desde REE y AEMET, y permite ver un resumen general de estos.

## El Pronóstico
