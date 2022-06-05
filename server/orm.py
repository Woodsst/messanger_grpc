import datetime
import json
import logging
import time

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

    async def create_log_for_room(self, room: str):
        self.cursor.execute(sql.SQL("""
        CREATE TABLE {}
            (
            member varchar NOT null,
            message varchar
            message_time date NOT null
            )
        """).format(sql.Identifier(room)))
        self.conn.commit()

    async def add_new_room(self, room_name: str, creator: str):
        try:
            self.cursor.execute(sql.SQL("""
            CREATE TABLE {}
            (
            creator varchar,
            member varchar NOT null,
            connection_time date NOT null
            )
            """).format(sql.Identifier(room_name)))
        except psycopg.errors.DuplicateTable:
            self.conn.commit()
            return False
        self.conn.commit()
        await self.add_creator_in_room(room_name, creator)
        await self.create_log_for_room(room_name)

    async def add_creator_in_room(self, room_name: str, creator: str):
        self.cursor.execute(sql.SQL("""
        INSERT INTO {} (creator, member, connection_time)
        VALUES (%s, %s, %s)
        """).format(sql.Identifier(room_name)),
                            (creator, creator, datetime.datetime.now()))
        self.conn.commit()

    async def add_friend(self, user_name: str, friend_name: str) -> bool:
        if await self.check_friend(friend_name, user_name):
            self.cursor.execute("""
            UPDATE clients 
            SET friend_list = array_append(friend_list, %(friend_name)s)
            WHERE username = %(username)s
            """, {
                "friend_name": friend_name,
                "username": user_name
            })
            self.conn.commit()
            return True
        return False

    async def check_friend_in_friend_list(self, friend_name: str, user_name: str) -> bool:
        self.cursor.execute("""
        SELECT array_position(friend_list, %(friend_name)s) 
        FROM clients 
        WHERE username=%(username)s
        """, {
            "friend_name": friend_name,
            "username": user_name
        })
        if self.cursor.fetchone()[0] is None:
            return False
        return True

    async def client_exist(self, client_name: str) -> bool:
        self.cursor.execute("""
        SELECT username 
        FROM clients
        WHERE username=%s 
        """, (client_name,))
        if self.cursor.fetchone() is None:
            return False
        return True

    async def remove_friend(self, friend_name: str, user_name: str) -> bool:
        if not await self.client_exist(friend_name):
            return False
        elif not await self.check_friend_in_friend_list(friend_name, user_name):
            return False
        self.cursor.execute("""
        UPDATE clients 
        SET friend_list = array_remove(friend_list, %(friend_name)s)
        WHERE username = %(username)s
        """, {
            "friend_name": friend_name,
            "username": user_name
        })
        self.conn.commit()
        return True

    async def check_friend(self, friend_name: str, user_name: str) -> bool:
        if not await self.client_exist(friend_name):
            return False
        elif await self.check_friend_in_friend_list(friend_name, user_name):
            return False
        return True

    async def join_room(self, username: str, room: str) -> bool:
        if await self.room_exist(room):
            self.cursor.execute(sql.SQL("""
            INSERT INTO {} (member, connection_time)
            VALUES (%s, %s)
            """).format(sql.Identifier(room)), (username, datetime.datetime.now()))
            self.conn.commit()
            return True
        return False

    async def room_escape(self, username: str, room: str) -> bool:
        if self.room_exist(room):
            self.cursor.execute(sql.SQL("""
            DELETE FROM {}
            WHERE member = %s
            """).format(sql.Identifier(room)), (username,))
            self.conn.commit()
            await self.delete_room_from_room_list(username, room)
            return True
        self.conn.commit()
        return False

    async def delete_room_from_room_list(self, username: str, room: str):
        self.cursor.execute("""
        UPDATE clients
        SET room_list = array_remove(room_list, %(room)s)
        WHERE username = %(username)s
        """, {"room": room,
              "username": username})
        self.conn.commit()

    async def room_exist(self, room):
        self.cursor.execute("""
        SELECT EXISTS (
            SELECT FROM 
                pg_tables
            WHERE 
                schemaname = 'public' AND 
                tablename  = %s
            )
        """, (room,))
        if self.cursor.fetchone()[0] is True:
            return True
        return False

    @staticmethod
    def data_to_dict(data: tuple) -> dict:
        result = {
            "username": data[0],
            "friend_list": data[1],
            "room_list": data[2]
        }
        result = json.dumps(result)
        return result
