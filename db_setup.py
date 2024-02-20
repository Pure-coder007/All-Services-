import mysql.connector
from models import config

def setup_database():
    config['database'] = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    

    # Users Table
    # cursor.execute('CREATE DATABASE IF NOT EXISTS crowd_funding')
    
    cursor.execute("""
    CREATE TABLE users (
    id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
    );
    """)

    

    connection.commit()
    cursor.close()
    connection.close()
  

if __name__ == "__main__":
        setup_database()
