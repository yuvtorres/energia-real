# archivo para leer de Red Eléctrica
from src.connect_db import client_mongo
from src.connect_db import client_influx
import requests
import json
import datetime as dt

def wigdet_caract():
    # función para el analisis de los endpoints de REE (2020 mayo)
    # apidatos.ree.es

    db=client_mongo.ereal_collections
    current=dt.datetime.now()
    # todos los endpoints de demanda
    widget_demanda=["evolucion","variacion-componentes", "variacion-componentes-movil",
    "ire", "ire-general", "ire-industria", "ire-servicios",  "ire-general-media",
    "demanda-maxima-diaria", "demanda-maxima-horaria",  "perdidas-transporte",
    "potencia-maxima-instantanea",  "variacion-demanda",  "potencia-maxima-instantanea-variacion",
    "potencia-maxima-instantanea-variacion-historico",   "demanda-tiempo-real",
    "variacion-componentes-anual", "variacion-demanda-mensual", "variacion-demanda-anual"]

    # todos los endpoints de generación
    widget_generacion= ["estructura-generacion","evolucion-renovable-no-renovable",
                    "estructura-renovables",
                    "estructura-generacion-emisiones-asociadas",
                    "evolucion-estructura-generacion-emisiones-asociadas",
                    "estructura-generacion-cuencas",
                    "no-renovables-detalle-emisiones-CO2",
                    "maxima-renovable",
                    "maxima-renovable-historico",
                    "maxima-sin-emisiones-historico",
                    "potencia-instalada"]

    # todos log endpoints de intercambios
    widget_intercambios=["francia-frontera",
                    "portugal-frontera",
                    "marruecos-frontera",
                    "andorra-frontera",
                    "francia-frontera-programado",
                    "portugal-frontera-programado",
                    "marruecos-frontera-programado",
                    "andorra-frontera-programado",
                    "enlace-baleares",
                    "frontera-fisicos",
                    "frontera-programados",
                    "intercambios-internacionales",
                    "total-frontera",
                    "francia-intercambios-fisicos"]

    # todos los endpoints de transporte
    widget_transporte=[ "energia-no-suministrada-ens",
                    "indice-indisponibilidad",
                    "tiempo-interrupcion-medio-tim",
                    "kilometros-lineas",
                    "ens-tim",
                    "indice-disponibilidad-total",
                    "tasa-mensual-disponibilidad-peninsular",
                    "tasa-mensual-disponibilidad-baleares",
                    "tasa-mensual-disponibilidad-canarias"]

    # todos los endpoints de mercados
    widget_mercados=["componentes-precio-energia-cierre-desglose",
                    "componentes-precio",
                    "energia-gestionada-servicios-ajuste",
                    "energia-restricciones",
                    "precios-restricciones",
                    "reserva-potencia-adicional",
                    "banda-regulacion-secundaria",
                    "energia-precios-regulacion-secundaria",
                    "energia-precios-regulacion-terciaria",
                    "energia-precios-gestion-desvios",
                    "coste-servicios-ajuste",
                    "volumen-energia-servicios-ajuste-variacion",
                    "precios-mercados-tiempo-real",
                    "energia-gestionada",
                    "coste-servicios-ajuses-variacion",
                    "energia-precios-ponderados-gestion-desvios-before",
                    "energia-precios-ponderados-gestion-desvios",
                    "energia-precios-ponderados-gestion-desvios-after"]
    res=[]
    url="https://apidatos.ree.es/es/datos/"
    
    endpoints=[widget_demanda,widget_generacion,widget_intercambios,
                widget_transporte,widget_mercados]
    end_str=['demanda','generacion','intercambios','transporte','mercados']
    k=0
    # **** consulta todos los endpoints 
    time_trunc="hour"
    for endp in endpoints:
        for wid in endp:
            widget=end_str[k]+"/"+wid
            query="?start_date="+str(current.year-1)+"-"+str(current.month).zfill(2)
            query+="-"+str(current.day-1).zfill(2)+"T"+str(current.hour-1).zfill(2)
            query+=":00&end_date="+str(current.year)+"-"+str(current.month).zfill(2)
            query+="-"+str(current.day).zfill(2)+"T"+str(current.hour-1).zfill(2)+":00&time_trunc="+time_trunc
#            query+="&geo_limit=peninsular"
            print("**** wid -> ",wid," ****")

            header={"Accept":"application/json",
                    "Content-Type":"application/json",
                    "Host":"apidatos.ree.es"}

            r=requests.get(url+widget+query, headers=header)
            json_d=r.json()
            print(json_d.keys())
            if 'errors' not in json_d.keys():
                res.append([end_str[k],wid,list(json_d.keys())])
        k+=1

    db.ree_hour.insert_many(res)
    return res

