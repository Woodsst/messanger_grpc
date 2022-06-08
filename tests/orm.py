import datetime

import psycopg

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
        DROP TABLE IF EXISTS log_r_test_room_1;
        DROP TABLE IF EXISTS log_test_user_2_test_user;
        """)
        self.conn.commit()

    def client_add(self, username: str, passwd: str, friend_list: set, room_list: set):
        friend_list = ''.join(x for x in str(friend_list) if x != "'")
        room_list = ''.join(x for x in str(room_list) if x != "'")
        self.cursor.execute("""
        INSERT INTO clients (username, passwd, registration_date, friend_list, room_list)
        VALUES (%(username)s, %(passwd)s, %(registration_date)s, %(friend_list)s, %(room_list)s)
        """, {
            "username": username,
            "passwd": passwd,
            "registration_date": datetime.datetime.now(),
            "friend_list": str(friend_list),
            "room_list": str(room_list)
        }
                            )
        self.conn.commit()

    def create_test_clients(self):
        self.client_add('test_user', 'asd1', {'test_user_1', 'test_user_2'},
                        {'r_test_room_1', 'r_test_room_2', 'r_test_room_3'})
        self.client_add('test_user_2', 'asasdd1', {'test_user', 'test_user_1', 'test_user_2'},
                        {'r_test_room_1', 'r_test_room_2'})
        self.client_add('test_user_3', 'asasdd1',
                        {'test_user_0'}, {'r_test_room_0'})
