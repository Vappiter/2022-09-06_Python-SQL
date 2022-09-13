from pickle import TRUE
import psycopg2
import re

RE_EMAIL = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
RE_PHONO = re.compile(r'^\(\d{3}\) \d{3}-\d{4}$')

def enter_input(client_db):
  count_attempt = 5
  var_input = ''
  while var_input != 'Q' and count_attempt > 0:
     var_input = input ('Что будем делать?\n\
     1 - Добавить клиента\n\
     2 - Добавить телефон к существующему клиенту\n\
     3 - Добавить Email к существующему клиенту\n\
     4 - Изменить данные существующего клиента\n\
     5 - Удалить телефон существующего клиента\n\
     6 - Удалить Email существующего клиента\n\
     7 - Удалить существующего клиента\n\
     8 - Поиск клиента\n\
     Q - Выход из программы\n').upper()
     count_attempt -= 1 
     if var_input == '1':
      return client_db.add_client(cur)
     elif var_input == 'O':
          return 'Q'
     elif var_input == 'I':
          return 'Q'
     elif var_input == 'Q':
          return 'Q'  
     elif count_attempt == 1:
          print('Извините нажата неизвестная клавиша\n\
               осталась последняя попытка.  :(')
     elif count_attempt == 0:   
          print('До свидания!!!')
          return 'Q'    
     else:
          print(f'Извините нажата неизвестная клавиша\n\
               Осталось {count_attempt} попыток! ;)')   

# Function create tables

def create_tab(cursor, name_tab):
    
     if name_tab == 'client':
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS client(
             id_client SERIAL PRIMARY KEY,
             firstname_client TEXT NOT NULL,
             lastname_client TEXT NOT NULL
        ); 
        """)
     elif name_tab == 'email':
          cursor.execute("""
               CREATE TABLE IF NOT EXISTS email(
                    id_email SERIAL PRIMARY KEY,
                    id_client INTEGER REFERENCES client (id_client),
                    name_email TEXT
               ); 
               """)
     elif name_tab == 'phono':   
          cursor.execute("""
               CREATE TABLE IF NOT EXISTS phono(
               id_phono SERIAL PRIMARY KEY,
               id_client INTEGER REFERENCES client (id_client),                    
               number_phono TEXT
               ); 
               """)
     else: print ('Таблица с таким именем не нужна')
     return           

# Enter firstname

def input_firstname():
     var_input_firstname = input ('Введите имя клиента: ').title()
     return var_input_firstname

# Enter lastname

def input_lastname():
     var_input_lastname = input ('Введите фамилию клиента: ').title()
     return var_input_lastname

# Enter Email

def input_email():
     var_input_email = input ('Введите email клиента: ')
     while re.fullmatch(RE_EMAIL, var_input_email) == None:
         print("Введен не правильный формат Email. Формат str@str.str")
         var_input_email = input ('Введите email клиента: ')
     return var_input_email   
          
# Enter Phono

def input_phono():
     var_input_phono = input ('Введите телефон клиента: ')
     while re.fullmatch(RE_PHONO, var_input_phono) == None:
         print("Не правильный формат телефона. Формат (222) 222-2222")
         var_input_phono = input ('Введите телефон клиента: ')
     return var_input_phono          
          
# Class working with the database

class Job_client:
     def __init__(self):
          pass
   
     
     def add_client(self, cursor):
       var_first_name = input_firstname()  
       var_last_name = input_lastname()
       var_name_email = input_email()
       var_number_phono = input_phono()
       cursor.execute ("""INSERT INTO client(firstname_client, lastname_client) VALUES (%s, %s)""", (var_first_name, var_last_name))
       conn.commit()
       cursor.execute(""" SELECT id_client FROM client WHERE firstname_client = %s AND lastname_client = %s""",(var_first_name, var_last_name))
       var_test = cursor.fetchall()
       var_id_client = str(var_test[0][0])
       cursor.execute ("""INSERT INTO email(id_client, name_email) VALUES (%s, %s)""", (var_id_client, var_name_email))
       cursor.execute ("""INSERT INTO phono(id_client, number_phono) VALUES (%s, %s)""", (var_id_client, var_number_phono))
       conn.commit()
       print('Клиент добавлен')
       return TRUE

# The main programm

if __name__ == '__main__':

 with psycopg2.connect(database="PythonSQL", user="vappiter", password="123456") as conn:
    with conn.cursor() as cur:
        
     # Creating tables in a database  
        
     create_tab (cur, "client")
     create_tab (cur, "email")
     create_tab (cur, "phono")
     
     # Working with the database
     
     client_db = Job_client()
     var_quit = ''
     while var_quit != 'Q': 
       var_exit = enter_input(client_db) 
       if var_exit == 'Q':
        quit()
     
    conn.commit()