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

## Visualización

La visualización se hace a través de una WEB que conecta a la API de análisis de datos para extraer los resultados.

### Instalación

1. Requisitos: python3, mongod, Influx, mariadb
2. Después de clonar (descargar), se deben instalar los módulos presentes en archivo requirements.txt 

	pip3 install -r requirements.txt

3. Crear el archivo .env en el directorio raiz, y definir las varibales de entorno:

- PORT_MONGO: puerto del servidor MONGO 
- HOST_MONGO: direccion del servidor MONGO
- PORT_INFLUX: puerto del servidor INFLUX
- HOST_INFLUX: direccion del servidor INFLUX
- USER_INFLUX: Usuario para interactuar con Influx
- PASSWORD_INFLUX: Clave del usuario
- AEMET_KEY: Clave para acceder al servidor de AEMET (solicitarla)
- REE_KEY: Clave para acceder al servidor de REE
- PORT: Puerto donde se define el servicio de e-real
