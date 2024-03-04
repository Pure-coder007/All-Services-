import mysql.connector
from models import config

def setup_database():
    config['database'] = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    

    # Users Table
    
    cursor.execute("""
    CREATE TABLE users (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    country VARCHAR(100),
    state VARCHAR(100),
    local_govt VARCHAR(100),
    address TEXT,
    profile_pic VARCHAR(255),
    PRIMARY KEY (id)
);


    """)

    cursor.execute("""
    CREATE TABLE workers (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    profile_pic VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    local_govt VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    service VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    rate DECIMAL(10,2) NOT NULL,
    work_pic1 VARCHAR(255) NOT NULL,
    work_pic2 VARCHAR(255) NOT NULL,
    work_pic3 VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

    """)



    cursor.execute("""
    CREATE TABLE contacts(
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

        """)
    


    cursor.execute("""
    CREATE TABLE worker_reviews(
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT(11) NOT NULL,
    worker_id INT(11) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    enjoy_service TINYINT(1) NOT NULL,
    suggestions TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (worker_id) REFERENCES workers(id)
);

     """)

    

    connection.commit()
    cursor.close()
    connection.close()
  

if __name__ == "__main__":
        setup_database()
