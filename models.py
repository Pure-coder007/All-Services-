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


config = {
    'user': 'root',
    'password': 'language007',
    'host': 'localhost',
    'database': 'all_services',
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
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        




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


def add_user(name, email, password):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, password))
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
