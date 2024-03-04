from flask import redirect, flash, url_for
import mysql.connector
from flask_login import UserMixin, LoginManager
# from db_setup import 
from datetime import datetime
from mysql.connector import Error
from werkzeug.utils import secure_filename
import os

login_manager = LoginManager()


import mysql.connector


# config = {
#     'user': 'root',
#     'password': 'language007',
#     'host': 'localhost',
#     'database': 'all_services',
#     'raise_on_warnings': True
# }



config = {
    'user': 'ukahdike007',
    'password': 'language007',
    'host': 'db4free.net',
    'database': 'ukahdike',
    'raise_on_warnings': True
}


conn = mysql.connector.connect(**config)


cursor = conn.cursor()


cursor.execute("SHOW TABLES;")
for table in cursor:
    print(table)


cursor.close()
conn.close()




conn = mysql.connector.connect(**config)




class User(UserMixin):
    def __init__(self, id, name, email, password, profile_pic, phone_number, country, state, local_govt, address):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.profile_pic = profile_pic
        self.phone_number = phone_number
        self.country = country
        self.state = state
        self.local_govt = local_govt
        self.address = address




class Worker(UserMixin):
    def __init__(self, id, name, email, password, profile_pic, phone_number, country, state, local_govt, address, company, service, description=None, rate=None, work_pic1=None, work_pic2=None, work_pic3=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.profile_pic = profile_pic
        self.phone_number = phone_number
        self.country = country
        self.state = state
        self.local_govt = local_govt
        self.address = address
        self.company = company
        self.service = service
        self.description = description
        self.rate = rate
        self.work_pic1 = work_pic1
        self.work_pic2 = work_pic2
        self.work_pic3 = work_pic3
       

        




    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    


def get_user(email):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
    user_record = cursor.fetchone()
    cursor.close()
    connection.close()
    print(user_record, 'user record')
    return user_record




def get_worker(email):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM workers WHERE email=%s', (email,))
    user_record = cursor.fetchone()
    cursor.close()
    connection.close()
    print(user_record, 'user record')
    return user_record

def add_user(name, email, password, profile_pic, phone_number, country, state, local_govt, address):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (name, email, password, profile_pic, phone_number, country, state, local_govt, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (name, email, password, profile_pic, phone_number, country, state, local_govt, address))
        connection.commit()
        cursor.close()
        connection.close()
        print('user added')
    except mysql.connector.Error as err:
        print(err)
        print('user not added')
    finally:
        cursor.close()
        connection.close()



def add_worker(name, email, password, profile_pic, phone_number, country, state, local_govt, address, company, service, description, rate, work_pic1, work_pic2, work_pic3):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO workers (name, email, password, profile_pic, phone_number, country, state, local_govt, address, company, service, description, rate, work_pic1, work_pic2, work_pic3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s , %s )', (name, email, password, profile_pic, phone_number, country, state, local_govt, address, company, service, description, rate, work_pic1, work_pic2, work_pic3))
        connection.commit()
        cursor.close()
        connection.close()
        print('worker added')
    except mysql.connector.Error as err:
        print(err)
        print('worker not added')
    finally:
        cursor.close()
        connection.close()

# print all user's name from db
def get_all_users():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    print(users)
    cursor.close()
    connection.close()
    return users


def get_user_id(user_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id=%s', (user_id,))
    user_record = cursor.fetchone()
    
    cursor.close()
    connection.close()

    if user_record:
        return User(
            id=user_record['id'],
            name=user_record['name'],
            email=user_record['email'],
            password=user_record['password'],
            profile_pic=user_record['profile_pic'],
            phone_number=user_record['phone_number'],
            country=user_record['country'],
            state=user_record['state'],
            local_govt=user_record['local_govt'],
            address=user_record['address'],           

        )
    
    return None


def get_worker_id(user_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM workers WHERE id=%s', (user_id,))
    user_record = cursor.fetchone()
    
    cursor.close()
    connection.close()

    if user_record:
        return User(
            id=user_record['id'],
            name=user_record['name'],
            email=user_record['email'],
            password=user_record['password'],
            profile_pic=user_record['profile_pic'],
            phone_number=user_record['phone_number'],
            country=user_record['country'],
            state=user_record['state'],
            local_govt=user_record['local_govt'],
            address=user_record['address'],
            company=user_record['company'],
            service=user_record['service'],
            description=user_record['description'],
            rate=user_record['rate'],
            work_pic1=user_record['work_pic1'],
            work_pic2=user_record['work_pic2'],
            work_pic3=user_record['work_pic3']         

        )
    
    return None



def contact_me(name, email, subject, message):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO contacts (name, email, subject, message) VALUES (%s, %s, %s, %s)", (name, email, subject, message))
        connection.commit()
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        connection.close()


def update_user_profile(user_id, name, email, phone_number, country, state, local_govt, address, profile_pic):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE users SET name=%s, email=%s, phone_number=%s, country=%s, state=%s, local_govt=%s, address=%s, profile_pic=%s WHERE id=%s",(name, email, phone_number, country, state, local_govt, address, profile_pic, user_id)
        )

        connection.commit()
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        connection.close()