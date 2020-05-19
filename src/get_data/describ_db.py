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
    [print(val['name']) for val in measu]

    print('* First and last registers *')
    for val in measu:
        print(f'First value in "{val["name"]}"')
        query_t=f'select first(value) from "{val["name"]}"'
        res=conn.client_influx.query(query_t)
        point=list(res.get_points(val['name']))
        print(point)

        print(f'Last value in "{val["name"]}"')
        query_t=f'select last(value) from "{val["name"]}"'
        res=conn.client_influx.query(query_t)
        point=list(res.get_points(val['name']))
        print(point)


