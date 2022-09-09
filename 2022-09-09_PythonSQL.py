import psycopg2

def create_tab(cursor, name_tab:str):
     if name_tab == 'client':
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS client(
             id_client SERIAL PRIMARY KEY,
             firstname_client TEXT,
             lastname_client TEXT
        ); 
        """)
     elif name_tab == 'email':
          cursor.execute("""
               CREATE TABLE IF NOT EXISTS %s(
                    id_%s SERIAL PRIMARY KEY,
                    _ TEXT
               ); 
               """, (name_tab,))
     elif name_tab == 'phono':   
          cursor.execute("""
               CREATE TABLE IF NOT EXISTS %s(
               id_client SERIAL PRIMARY KEY,
               lastname_client TEXT
               ); 
               """, (name_tab,))
     else: print ('Таблица с таким именем не нужна')
     return           


with psycopg2.connect(database="PythonSQL", user="postgres", password="123456") as conn:
   with conn.cursor() as con:
     cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
             id_client SERIAL PRIMARY KEY,
             lastname_client TEXT
        ); 
        """)
     # create_tab (con, 'email')

     conn.commit()