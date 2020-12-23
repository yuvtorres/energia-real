# Object connections and constants
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from src.connect_db import client_influx
from src.connect_db import client_mongo

# libraries from python 
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import statsmodels.api as sm
import datetime as dt

def make_gen_eo():
    # función que hace el pronóstico de generación eólico usando redes
    # neuronales. También crea la gráfica de estaciónes

    # carga datos de generación históticos recientes
    q_str=''' SELECT * FROM "Generación T.Real eólica"  WHERE time > now()-3d'''
    res=client_influx.query_api().query(q_str,org='ereal')

    points=res.items()
    points=list(points)
    g_eo=points[0][1]
    print('+ Se han importado ',len(g_eo), ' datos de generación eólica')

    # carga datos de viento medio
    q_str=''' SELECT * FROM "Clima"  WHERE time > now()-3d'''
    res=client_influx.query_api().query(q_str,org='ereal')

    points=res.items()
    points=list(points)
    clima=points[0][1]
    col_velmedia=[ele for ele in clima.columns if ele.split('-')[0]=='velmedia']
    clima_velmedia=clima[[*col_velmedia]]
    clima_velmedia=clima_velmedia.drop(['velmedia'],axis=1)
    rename={old:old.split('-')[-1] for old in clima_velmedia}
    clima_velmedia=clima_velmedia.rename(columns=rename)
    clima_velmedia=clima_velmedia.dropna(axis='columns')
    clima_velmedia=filtro_geo_estacion(clima_velmedia)

    # chequeo georeferencia
    db= client_mongo.ereal_collections
    estaciones=list(db.estaciones.find({},{'_id':0,'indicativo':1}))

    print('+ Se han importado ',clima_velmedia.shape[0], ' medidas de viento')
    print('+ Que corresponde con ',clima_velmedia.shape[1], ' columnas')

    # Modelo de predicción
    data=clima_velmedia.join(g_eo)
    data=data.drop(['geo_id'],axis=1)
    data=data.dropna()
    print()
    print('Los datos para el modelo son de dimensión:', data.shape)
    
    print('Tiene ', sum( data.isna().sum() ) , ' nulos')

    y=data['value']
    X=data[[*[col for col in data.columns if col!='value']]]
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    regr = MLPRegressor(hidden_layer_sizes=120,activation='logistic',
            random_state=1, max_iter=500,solver='lbfgs').fit(X_train, y_train)

    r2=regr.score(X_test, y_test)
    print('El r2 del modelo es',r2)

    db=client_mongo.ereal_collections
    db.scores.insert_one({'name':'eolico','data':dt.datetime.now(),'r2':r2})

    #carga las estaciones con cluster
    df_estaciones=pd.read_csv('data/estaciones.csv')
    clusters=list(df_estaciones.cluster.value_counts().index)
    X_pred=pd.DataFrame()
    
    for cluster in clusters:
        pred=pd.read_csv('data/pred_wind_'+str(cluster)+'.csv')
        pred=pred.rename({'Unnamed: 0': 'time'}, axis='columns')
        pred.time=pd.to_datetime(pred.time)
        pred=pred.set_index('time')
        if len(X_pred)==0:
            X_pred=pred
        else:
            X_pred=X_pred.join(pred,how='inner')

    y_predict=regr.predict(X_pred)
    y_predict=pd.DataFrame(y_predict).set_index(X_pred.index)
    
    print(y.index)
    print(y_predict.index)
    plt.plot(y)
    plt.plot(y_predict)
    plt.savefig('src/templates/pred_eo.png')




def filtro_geo_estacion(clima_velmedia):
    # chequeo georeferencia
    db= client_mongo.ereal_collections
    estaciones=list(db.estaciones.find({},{'_id':0,'indicativo':1}))
    for col in clima_velmedia.columns:
        if len(list(db.estaciones.find({'indicativo':col},{}) ) )==0:
            clima_velmedia=clima_velmedia.drop([col], axis=1)

    return clima_velmedia


