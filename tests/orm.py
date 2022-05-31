import psycopg
import datetime
from config import Settings


class Orm:
    def __init__(self, config: Settings):
        self.config = config
        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self):
        conn = psycopg.connect(dbname=self.config.db_name,
                               user=self.config.db_username,
                               host=self.config.db_host,
                               port=self.config.db_port,
                               password=self.config.db_password)
        return conn

    def delete_test_client(self):
        self.cursor.execute("""
        DELETE FROM clients WHERE username='test_user';
        """)
        self.conn.commit()

    def test_client_add(self):
        self.cursor.execute("""
        INSERT INTO clients (username, passwd, registration_date, friend_list, room_list)
        VALUES (%(username)s, %(passwd)s, %(registration_date)s, %(friend_list)s, %(room_list)s)
        """, {
            "username": "test_user",
            "passwd": "12l3k",
            "registration_date": datetime.datetime.now(),
            "friend_list": "{test_client_1, test_client_2}",
            "room_list": "{test_room_1, test_room_2}"
        }
        )
        self.conn.commit()

