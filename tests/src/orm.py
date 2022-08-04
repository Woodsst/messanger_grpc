import time

import psycopg
from psycopg import sql

from tests.src.config import Settings


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
        DELETE FROM clients WHERE username='test_user_2';
        DELETE FROM clients WHERE username='test_user_3';
        """)
        self.conn.commit()

    def clearing_database(self):
        self.delete_test_client()
        self.delete_test_room()

    def delete_test_room(self):
        self.cursor.execute("""
        DROP TABLE IF EXISTS log_r_test_room;
        DROP TABLE IF EXISTS r_test_room;
        DROP TABLE IF EXISTS r_test_room_1;
        DROP TABLE IF EXISTS r_test_room_2;
        DROP TABLE IF EXISTS log_r_test_room_1;
        DROP TABLE IF EXISTS log_r_test_room_2;
        DROP TABLE IF EXISTS log_test_user_2_test_user;
        """)
        self.conn.commit()

    def client_add(self, username: str, passwd: str):
        self.cursor.execute("""
        INSERT INTO clients (username, passwd, registration_date)
        VALUES (%(username)s, %(passwd)s, %(registration_date)s)
        """, {
            "username": username,
            "passwd": passwd,
            "registration_date": int(time.time()),
        }
                            )
        self.conn.commit()

    def create_test_clients(self):
        self.client_add('test_user', 'asd1')
        self.client_add('test_user_2', 'asasdd1')
        self.client_add('test_user_3', 'asasdd1')

    def write_message_in_log(self, log: str, username: str, message: str, message_time: int):
        self.cursor.execute(sql.SQL("""
        INSERT INTO {} (member, message, message_time)
        VALUES (%s, %s, %s)
        """).format(sql.Identifier(log)),
                            (username, message, message_time))
        self.conn.commit()

    def create_messages_in_room(self):
        self.write_message_in_log('log_r_test_room_1', 'test_user_1',
                                  'Hello_1', 1655103816)
        self.write_message_in_log('log_r_test_room_1', 'test_user_1',
                                  'Hello_2', 1655103817)
        self.write_message_in_log('log_r_test_room_1', 'test_user_1',
                                  'Hello_3', 1655103818)
        self.write_message_in_log('log_r_test_room_1', 'test_user_1',
                                  'Hello_4', 1655103819)
