# Module with the basic analisys from the database.

import src.config
import src.connect_db as conn

def describ_db():
    query_api = conn.client_influx.query_api()
    c_mongo = conn.client_mongo
    db=c_mongo.ereal_collections


    print('*** Influx db description ***')
    print('***  the dbs are:')
    print(f'the value of db is: {db}, and the type is: {type(db)}')
    [ print(val['name']) for val in db if val['name']!='_internal' ]
    print('                ***')
    
    conn.client_influx.switch_database('db_ereal')
    measu=conn.client_influx.get_list_measurements()
    print('** The measurements **')

    for val in measu:
        query_t=f'select first(value) from "{val["name"]}"'
        res=conn.client_influx.query(query_t)
        point_f=list(res.get_points(val['name']))

        query_t=f'select last(value) from "{val["name"]}"'
        res=conn.client_influx.query(query_t)
        point_l=list(res.get_points(val['name']))
        point_f=[ele["time"] for ele in point_f]
        point_l=[ele["time"] for ele in point_l]

        if len(point_f)==0:
            print('Measure without time')
        else:
            print(f''''The measure: "{val["name"]}" {point_f[0]}- {point_l[0]}''')
            data={'$set':{'name':val['name'],'f_data':point_f[0],'l_data':point_l[0]}}
            db.descrip.update_one({'name':val['name']},data,upsert=True)
        

