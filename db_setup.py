import mysql.connector
from models import config

def setup_database():
    config['database'] = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    

    # Users Table
    
    cursor.execute("""
    CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    country VARCHAR(100),
    state VARCHAR(100),
    local_govt VARCHAR(100),
    address TEXT,
    profile_pic VARCHAR(255)
);

    """)

    

    connection.commit()
    cursor.close()
    connection.close()
  

if __name__ == "__main__":
        setup_database()
