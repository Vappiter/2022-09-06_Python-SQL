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
     elif var_input == '2':
          return client_db.add_phono(cur)
     elif var_input == '3':
          return client_db.add_email(cur)
     elif var_input == '4':
          return client_db.edit_client(cur)
     elif var_input == '5':
          return client_db.delete_phono(cur)
     elif var_input == '6':
          return client_db.delete_email(cur)
     elif var_input == '7':
          return client_db.search_client(cur)
     elif var_input == '8':
          return client_db.search_client(cur)  
     elif count_attempt == 1:
          print('Извините нажата неизвестная клавиша\n\
               осталась последняя попытка.  :(')
     elif count_attempt == 0:   
          print('До свидания!!!')
          return 'Q'   
     elif var_input == 'Q':
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
     var_input_email = input ('Введите email клиента. Формат str@str.str: ')
     while re.fullmatch(RE_EMAIL, var_input_email) == None:
         print("Введен не правильный формат Email. Формат str@str.str")
         var_input_email = input ('Введите email клиента. Формат str@str.str: ')
     return var_input_email   
          
# Enter Phono
def input_phono():
     var_input_phono = input ('Введите телефон клиента. Формат (222) 222-2222: ')
     while re.fullmatch(RE_PHONO, var_input_phono) == None:
         print("Не правильный формат телефона. Формат (222) 222-2222")
         var_input_phono = input ('Введите телефон клиента. Формат (222) 222-2222": ')
     return var_input_phono          
          
# Class working with the database

class Job_client:
     def __init__(self):
          pass
   
     # Add client
     
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
  
  # Аdd a phono to an existing client 
  
     def add_phono (self, cursor):
       var_first_name = input_firstname()  
       var_last_name = input_lastname()
       cursor.execute(""" SELECT id_client, firstname_client, lastname_client FROM client WHERE firstname_client = %s AND lastname_client = %s""",(var_first_name, var_last_name))
       var_test = cursor.fetchall()
       print(f'Этому клиенту {var_test[0][1]} {var_test[0][2]} будем добавлять телефон? Y/n')
       var_input_switch = input().upper()
       if var_input_switch == 'Y':
        var_id_client = str(var_test[0][0])
        var_number_phono = input_phono()
        cursor.execute ("""INSERT INTO phono(id_client, number_phono) VALUES (%s, %s)""", (var_id_client, var_number_phono))
        conn.commit()
        print(f'Телефон {var_number_phono} клиенту {var_test[0][1]} {var_test[0][2]} добавлен')
        return TRUE
       else:
          return print ('Извините, такого клиента нет :(. Добавьте клиента, пожалуйста') 
       
 # Add a Email to an existing client
 
     def add_email (self, cursor):
       var_first_name = input_firstname()  
       var_last_name = input_lastname()
       cursor.execute(""" SELECT id_client, firstname_client, lastname_client FROM client WHERE firstname_client = %s AND lastname_client = %s""",(var_first_name, var_last_name))
       var_test = cursor.fetchall()
       print(f'Этому клиенту {var_test[0][1]} {var_test[0][2]} будем добавлять Email? Y/n')
       var_input_switch = input().upper()
       if var_input_switch == 'Y':
        var_id_client = str(var_test[0][0])
        var_name_email = input_email()
        cursor.execute ("""INSERT INTO email(id_client, name_email) VALUES (%s, %s)""", (var_id_client, var_name_email))
        conn.commit()
        print(f'Email {var_name_email} клиенту {var_test[0][1]} {var_test[0][2]} добавлен')
        return TRUE
       else:
          return print ('Извините, такого клиента нет :(. Добавьте клиента, пожалуйста')
     
 # Edit data existing client ENTER_SWITCH
     
     def edit_client(self, cursor):
          print ('Необходимо ввести имя и фамилию клиента у которого хотим изменить данные\n')
          var_first_name = input_firstname()  
          var_last_name = input_lastname()
          cursor.execute(""" SELECT id_client, firstname_client, lastname_client FROM client WHERE firstname_client = %s AND lastname_client = %s""",(var_first_name, var_last_name))
          var_test = cursor.fetchall()
          count_attempt = 5
          if var_test == []:
           return print ('Извините, такого клиента нет :(. Добавьте клиента, пожалуйста')
          else:
              var_input = input (f'Что будем делать с клиентом {var_test[0][1]} {var_test[0][2]}?\n\
          1 - Редактировать телефоны клиента\n\
          2 - Редактировать Email клиента\n\
          3 - Редактировать имя и фамилию клиента\n\
          Q - Выход из редактирования клиента\n').upper()
          count_attempt -= 1 
          if var_input == '1':
           return client_db.edit_phono(cur,var_test[0][0],var_test[0][1],var_test[0][2])
          elif var_input == '2':
             return client_db.edit_email(cur,var_test[0][0],var_test[0][1],var_test[0][2])
          elif var_input == '3':
             return client_db.edit_client_two(cur,var_test[0][0],var_test[0][1],var_test[0][2] )
          elif count_attempt == 1:
             print('Извините нажата неизвестная клавиша\n\
               осталась последняя попытка.  :(')
          elif count_attempt == 0:   
             print('До свидания!!!')
             return 'Q'   
          elif var_input == 'Q':
             return 'Q'
          else:
             print(f'Извините нажата неизвестная клавиша\n\
               Осталось {count_attempt} попыток! ;)') 
     
    # Edit data existing client 
     
     def edit_client_two(self, cursor, var_id_client, var_firstname_client, var_lastname_client):
          print (f'У клиента сейчас имя {var_firstname_client}. Будем редактировать Y/n')
          var_input_switch = input().upper()
          if var_input_switch == 'Y':
           var_first_name = input_firstname()    
           cursor.execute ("""UPDATE client SET firstname_client = %s WHERE id_client = %s""", (var_first_name, var_id_client))
           conn.commit()
           print (f'У клиента сейчас фамилия {var_lastname_client}. Будем редактировать Y/n')
          var_input_switch = input().upper()
          if var_input_switch == 'Y':
           var_last_name = input_lastname()    
           cursor.execute ("""UPDATE client SET lastname_client = %s WHERE id_client = %s""", (var_last_name, var_id_client))
           conn.commit()
          return print(f'Редактирование имени и фамилии завершено')
          
    # Edit phono existing client
   
     def edit_phono(self, cursor, var_id_client, var_firstname_client, var_lastname_client):
       print(f'К клиенту {var_firstname_client} {var_lastname_client} привязаны следующие телефоны:\n')   
       cursor.execute(""" SELECT id_phono, number_phono FROM phono WHERE id_client = %s""",(str(var_id_client))) 
       var_test = cursor.fetchall()
       print (var_test)
       print (f'Будем редактировать Y/n')
       var_input_switch = input().upper()
       if var_input_switch == 'Y':
        print('Нужно ввести номер телефона, который будем редактировать. Формат (222) 222-2222:')    
        var_edit_phono = input_phono()
        cursor.execute(""" SELECT id_phono FROM phono WHERE number_phono = %s""",(var_edit_phono,)) 
        var_test_phono = cursor.fetchall()
        print(f'НОВЫЙ НОМЕР \n')    
        var_new_phono = input_phono()
        cursor.execute ("""UPDATE phono SET number_phono = %s WHERE id_phono = %s""", (var_new_phono, var_test_phono[0][0]))
        conn.commit()
       return print(f'\n Редактирование телефона завершено')
  
     # Edit email existing client
   
     def edit_email(self, cursor, var_id_client, var_firstname_client, var_lastname_client):
       print(f'К клиенту {var_firstname_client} {var_lastname_client} привязаны следующие Email:\n')   
       cursor.execute("""SELECT id_email, name_email FROM email WHERE id_client = %s""",(str(var_id_client))) 
       var_test = cursor.fetchall()
       print (var_test)
       print (f'Будем редактировать Y/n')
       var_input_switch = input().upper()
       if var_input_switch == 'Y':
        print('Нужно ввести Email, который будем редактировать. Формат str@str.str:')    
        var_edit_email = input_email()
        cursor.execute("""SELECT id_email FROM email WHERE name_email = %s""",(var_edit_email,)) 
        var_test = cursor.fetchall()
        print(f'НОВЫЙ Email\n')    
        var_new_email = input_email()
        cursor.execute ("""UPDATE email SET name_email = %s WHERE id_email = %s""", (var_new_email, var_test[0][0]))
        conn.commit() 
       return print(f'\n Редактирование Email завершено')  
               
 # Delete a phono to an existing client 
  
     def delete_phono (self, cursor):
          print ('Необходимо ввести имя и фамилию клиента Email которого хотим удалить\n')
          var_first_name = input_firstname()  
          var_last_name = input_lastname()
          cursor.execute(""" SELECT id_client FROM client WHERE firstname_client = %s AND lastname_client = %s""",(var_first_name, var_last_name))
          var_test = cursor.fetchall()
          if var_test == []:
           return print ('Извините, такого клиента нет :(. Добавьте клиента, пожалуйста')
          else:    
             var_id_client = str(var_test[0][0])
             cursor.execute(""" DELETE FROM phono WHERE id_client = %s""",(var_id_client))
             return print (f'У клиента {var_first_name} {var_last_name} удалены телефоны из БД')
     
 # Delete a Email to an existing client
 
     def delete_email (self, cursor):
          print ('Необходимо ввести имя и фамилию клиента Email которого хотим удалить\n')
          var_first_name = input_firstname()  
          var_last_name = input_lastname()
          cursor.execute(""" SELECT id_client FROM client WHERE firstname_client = %s AND lastname_client = %s""",(var_first_name, var_last_name))
          var_test = cursor.fetchall()
          if var_test == []:
           return print ('Извините, такого клиента нет :(. Добавьте клиента, пожалуйста')
          else:    
             var_id_client = str(var_test[0][0])
             cursor.execute(""" DELETE FROM email WHERE id_client = %s""",(var_id_client))
             return print (f'У клиента {var_first_name} {var_last_name} удалены Email из БД')
 
 # Delete existing client
 
     def delete_client (self, cursor):
          print ('Необходимо ввести имя и фамилию клиента которого хотим удалить\n')
          var_first_name = input_firstname()  
          var_last_name = input_lastname()
          cursor.execute(""" SELECT id_client FROM client WHERE firstname_client = %s AND lastname_client = %s""",(var_first_name, var_last_name))
          var_test = cursor.fetchall()
          if var_test == []:
           return print ('Извините, такого клиента нет :(. Добавьте клиента, пожалуйста')
          else:    
             var_id_client = str(var_test[0][0])
             cursor.execute(""" DELETE FROM email WHERE id_client = %s""",(var_id_client))
             cursor.execute(""" DELETE FROM phono WHERE id_client = %s""",(var_id_client))
             cursor.execute(""" DELETE FROM client WHERE id_client = %s""",(var_id_client))
             return print (f'Клиент {var_first_name} {var_last_name} удален из БД')   
     
 # Search existing client
 
     def search_client (self, cursor):
          var_first_name = input_firstname()  
          var_last_name = input_lastname()
          cursor.execute(""" SELECT id_client, firstname_client, lastname_client FROM client WHERE firstname_client = %s AND lastname_client = %s""",(var_first_name, var_last_name))
          var_test = cursor.fetchall()
          if var_test == []:
           return print ('Извините, такого клиента нет :(. Добавьте клиента, пожалуйста')
          else:    
             var_id_client = str(var_test[0][0])
             cursor.execute(""" SELECT name_email FROM email WHERE id_client = %s""",(var_id_client))
             var_test_email = cursor.fetchall()
             cursor.execute(""" SELECT number_phono FROM phono WHERE id_client = %s""",(var_id_client))
             var_test_phono = cursor.fetchall()
             return print (var_test, var_test_email, var_test_phono)
     
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