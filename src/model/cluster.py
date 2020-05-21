# Object connections and constants
from statsmodels.tsa.api import SARIMAX
from sklearn.cluster import KMeans
from src.connect_db import client_influx
from src.connect_db import client_df
from src.connect_db import client_mongo

# libraries from python 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import statsmodels.api as sm

def crea_cluster():
    # función que asigna a cada estación meterologica un cluster según su
    # latitud longitud. También crea la gráfica de estaciónes

    db=client_mongo.ereal_collections
    estaciones=list(db.estaciones.find({},{'_id':0,'indicativo':1,'latitud':1,'longitud':1}))
    estaciones_k=np.array( [ [ int(ele['latitud'][:-1]) ,
               (-1 if ele['longitud'][-1]=='W' else 1)*int(ele['longitud'][:-1]) ]
               for ele in estaciones ] )

    # aqui es donde se define el número de clusters
    kmeans = KMeans(n_clusters=20, random_state=0).fit(estaciones_k)

    cluster=kmeans.predict(estaciones_k)
    plt.scatter(estaciones_k.T[1],estaciones_k.T[0],c=list(cluster))
    plt.savefig('src/templates/mapa_estaciones.png')
    
    lat=[int(ele['latitud'][:-1]) for ele in estaciones]
    lon=[(-1 if ele['longitud'][-1]=='W' else 1)*int(ele['longitud'][:-1]) for ele in estaciones]
    indicativo=[ele['indicativo'] for ele in estaciones]

    df_estaciones=pd.DataFrame(data={'lat':lat,
        'lon':lon,'indicativo':indicativo,'cluster':list(cluster)})
    df_estaciones.to_csv('data/estaciones.csv')

def make_winds():
    # función que hace la predicción del tiempo del día siguiente con base en
    # las últimas medidas de viento y agrupando por clusters
    
    #carga las estaciones con cluster
    df_estaciones=pd.read_csv('data/estaciones.csv')
    clusters=list(df_estaciones.cluster.value_counts().index)

    # lee las medidas de Influx y las pone como dataframe
    df=client_df
    q_str=''' SELECT * FROM "Clima"  WHERE time > now()-3d'''
    res=df.query(q_str)
    points=res.items()
    points=list(points)
    clima=points[0][1]
    col_velmedia=[ele for ele in clima.columns if ele.split('-')[0]=='velmedia']
    clima_velmedia=clima[[*col_velmedia]]
    clima_velmedia.shape
    clima_velmedia=clima_velmedia.drop(['velmedia'],axis=1)
    rename={old:old.split('-')[-1] for old in clima_velmedia}
    clima_velmedia=clima_velmedia.rename(columns=rename)
    clima_velmedia=clima_velmedia.dropna(axis='columns')

    #Asigna cluster a las medidas de los últimas lecturas
    df_clima_est=df_estaciones.loc[df_estaciones['indicativo'].isin(list(clima_velmedia.columns))]
    plt.scatter(df_clima_est['lon'],df_clima_est['lat'],c=df_clima_est['cluster'])
    plt.savefig('src/templates/mapa_estaciones_lec.png')
    r2_vec=[]    
    df_clima_est=df_clima_est.set_index('indicativo')
    for cluster in clusters:
        #filtra por cluster
        cv_x=clima_velmedia[[*list(df_clima_est.loc[df_clima_est['cluster']==cluster].index)]]
        if len(cv_x.columns)>1:
            mod = sm.tsa.VARMAX(cv_x, order=(5,0), trend='n')
            res = mod.fit(maxiter=1000, disp=False)
            r2_vec.append(res.mse)
            cv_x_pred = res.forecast(24)
            cv_x_pred.to_csv('data/pred_wind_'+str(cluster)+'.csv')
        else:
            sarimax_mod = SARIMAX(cv_x, order=((1,12,24),0, 0), trend='n')
            try: 
                sarimax_res = sarimax_mod.fit()
            except:
                sarimax_mod = SARIMAX(cv_x, order=((1,24),0, 0), trend='n')
                sarimax_res = sarimax_mod.fit()

            cv_x_pred=sarimax_res.forecast(24)
            r2_vec.append(sarimax_res.mse)
            cv_x_pred=cv_x_pred.rename(cv_x.columns[0])
            cv_x_pred.to_csv('data/pred_wind_'+str(cluster)+'.csv')
 

    return r2_vec
