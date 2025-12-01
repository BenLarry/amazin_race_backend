import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host= os.getenv("HOST"),
            port=os.getenv("PORT"),
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            autocommit=True
        )

    def get_conn(self):
        return self.conn