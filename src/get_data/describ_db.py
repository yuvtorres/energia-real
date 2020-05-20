import src.config
import src.connect_db as conn

def describ_db():
    dbs = conn.client_influx.get_list_database()

    print('*** Influx db description ***')
    print('***  the dbs are:')
    [ print(val['name']) for val in dbs if val['name']!='_internal' ]
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
        print(f''''The measure: "{val["name"]}" {[ele["time"] for ele in point_f]}- {[ele["time"] for ele in point_l]}''')


