import os
import mysql.connector

def load_env_file(file_path=".env"):
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
load_env_file()

db_config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWD"),   
    'host': 'localhost',               
    'database': os.getenv("DB_NAME")            
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
