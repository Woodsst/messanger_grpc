import datetime
import logging
import time
import json

import psycopg
from psycopg import sql

from server.config import Settings

logger = logging.getLogger()


class Orm:
    def __init__(self, config: Settings):
        self.config = config
        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self) -> psycopg.Connection:
        timeout = 0.1
        connect = False
        while not connect:
            time.sleep(timeout)
            try:
                conn = psycopg.connect(dbname=self.config.db_name,
                                       user=self.config.db_username,
                                       password=self.config.db_password,
                                       host=self.config.db_host,
                                       port=self.config.db_port)
            except psycopg.OperationalError:
                timeout += 0.1
                if timeout > 0.5:
                    logger.critical('Error - connect to database host: %s, port: %s',
                                    self.config.db_host, self.config.db_port)
                    raise psycopg.OperationalError('connection with database failed')
                continue
            connect = True
        return conn

    async def get_client_information(self, name: str) -> dict or bool:
        self.cursor.execute("""
        SELECT username, friend_list, room_list
        FROM clients
        WHERE username=%(username)s
        """, {'username': name})
        information = self.cursor.fetchone()

        if information is None:
            return False

        information = self.data_to_dict(information)
        self.conn.commit()
        return information

    async def add_new_room(self, room_name: str, creator: str):
        room_name = f'r_{room_name}'
        self.cursor.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {}
        (
        creator varchar,
        member varchar NOT null,
        message varchar NOT null,
        message_time date NOT null
        )
        """).format(sql.Identifier(room_name)))
        self.conn.commit()
        self.cursor.execute(sql.SQL("""
        INSERT INTO {} (creator, message_time, member, message)
        VALUES (%s, %s, %s, '')
        """).format(sql.Identifier(room_name)),
                            (creator, datetime.datetime.now(), creator))
        self.conn.commit()

    @staticmethod
    def data_to_dict(data: tuple) -> dict:
        result = {
            "username": data[0],
            "friend_list": data[1],
            "room_list": data[2]
        }
        result = json.dumps(result)
        return result
