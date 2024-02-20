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
    'database': 'my_services',
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
    def __init__(self, id, email, password, username, phone_number, is_worker, is_admin, profile_picture=None, work_pic1=None, work_pic2=None, work_pic3=None):
        self.id = id
        self.email = email
        self.password = password
        self.username = username
        self.phone_number = phone_number
        self.is_worker = is_worker
        self.profile_picture = profile_picture
        self.work_pic1 = work_pic1
        self.work_pic2 = work_pic2
        self.work_pic3 = work_pic3
        self.is_admin = is_admin




    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False