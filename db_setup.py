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
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(100) NOT NULL,
    is_worker TINYINT(1) NOT NULL,
    profile_picture VARCHAR(255),
    category VARCHAR(50),
    location VARCHAR(100),
    city VARCHAR(100),
    rate VARCHAR(50),
    open_for_video_calls TINYINT(1),
    bio TEXT,
    work_pic1 VARCHAR(255),
    work_pic2 VARCHAR(255),
    work_pic3 VARCHAR(255)
    );

    """)
    


    # Workers Table
    cursor.execute("""
    CREATE TABLE workers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    city VARCHAR(100),
    phone_number VARCHAR(100) NOT NULL,
    rate DECIMAL(10, 2) NOT NULL,
    open_for_video_calls BOOLEAN NOT NULL,
    bio TEXT
);
    """)

    cursor.execute("""
    CREATE TABLE worker_reviews(
    id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT(11) NOT NULL,
    worker_id INT(11) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(100) NOT NULL,
    enjoy_service TINYINT(1),
    suggestions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (worker_id) REFERENCES users(id)
);
    """)


    

    connection.commit()
    cursor.close()
    connection.close()
  

if __name__ == "__main__":
        setup_database()
