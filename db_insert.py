import psycopg2 as pg

def connect_db():
    conn = pg.connect(
    database="atlys_db", user='postgres', password='postgres', host='localhost', port='5439'
    )

    return conn


def insert_values(df, table): 

    # tuples = [tuple(x) for x in df.to_numpy()] 
    conn = connect_db()

    cols = ','.join(list(df.columns)) 
    # SQL query to execute 
    text = "INSERT INTO %s(%s) VALUES " % (table, cols,) 
    values_txt = str(list(df.to_records(index=False)))
    values_txt = values_txt.replace('[', '')
    values_txt = values_txt.replace(']', '')
    query = text + values_txt
    cursor = conn.cursor() 
    try: 
        cursor.execute(query)
        conn.commit()
        print("Data inserted to database") 
    except (Exception, pg.DatabaseError) as error: 
        print("Error: %s" % error) 
        conn.rollback()
    
    cursor.close() 