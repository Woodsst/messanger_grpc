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

    async def update_friend_logs(self, username: str, friend_list: list, update_time: int) -> dict:
        update_friend_messages = {}
        for friend in friend_list:
            log = await self.check_friend_log_exist(friend, username)
            if log:
                update = await self.check_update_in_log(log, update_time)
                if update is not False:
                    update_friend_messages[friend] = update
        return update_friend_messages

    async def update_room_logs(self, room_list: list, update_time: int) -> dict:
        update_room_messages = {}
        for room in room_list:
            room = f'log_{room}'
            if await self.table_exist(room):
                update = await self.check_update_in_log(room, update_time)
                update_room_messages[room] = update
        return update_room_messages

    async def check_update_in_log(self, log_name: str, update_time: int):
        self.cursor.execute(sql.SQL("""
        SELECT * 
        FROM {}
        WHERE message_time > %s
        """).format(sql.Identifier(log_name)), (update_time,))
        result = self.cursor.fetchall()
        self.conn.commit()
        if len(result) > 0:
            return result
        return False

    async def message_in_room(self, message: str, addressee: str, user: str) -> bool:
        if await self.table_exist(addressee) and await self.check_room_in_room_list(user, addressee):
            addressee = f'log_{addressee}'
            self.cursor.execute(sql.SQL("""
            INSERT INTO {} (member, message, message_time)
            VALUES (%(member)s, %(message)s, %(message_time)s)
            """).format(sql.Identifier(addressee)),
                                {"member": user,
                                 "message": message,
                                 "message_time": int(time.time())})
            self.conn.commit()
            return True
        return False

    async def check_room_in_room_list(self, username: str, room_name: str) -> bool:
        self.cursor.execute("""
        SELECT array_position(room_list, %(room_name)s)
        FROM clients
        WHERE username=%(username)s
        """, {"room_name": room_name,
              "username": username})
        if self.cursor.fetchone()[0] is None:
            return False
        return True

    async def message_for_friend(self, message: str, addressee: str, username: str) -> bool:
        if await self.check_friend_in_friend_list(addressee, username):
            log_name = await self.create_log_friend_chat(addressee, username)
            self.cursor.execute(sql.SQL("""
            INSERT INTO {} (member, message, message_time)
            VALUES (%(member)s, %(message)s, %(message_time)s)
            """).format(sql.Identifier(log_name)),
                                {"member": username,
                                 "message": message,
                                 "message_time": int(time.time())
                                 })
            self.conn.commit()
            return True
        return False

    async def check_friend_log_exist(self, addressee: str, username: str) -> str or bool:
        first = f'log_{addressee}_{username}'
        second = f'log_{username}_{addressee}'
        if await self.table_exist(first):
            return first
        if await self.table_exist(second):
            return second
        return False

    async def create_log_friend_chat(self, addressee: str, username: str) -> str:
        log_name = await self.check_friend_log_exist(addressee, username)
        if log_name is False:
            log_name = f'{addressee}_{username}'
            await self.create_log_for_room(log_name)
            return f'log_{log_name}'
        return log_name

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
        room = f'log_{room}'
        self.cursor.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {}
            (
            member varchar NOT null,
            message varchar,
            message_time int NOT null
            )
        """).format(sql.Identifier(room)))
        self.conn.commit()

    async def add_new_room(self, room_name: str, creator: str) -> bool:
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
        return True

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
        if await self.table_exist(room):
            self.cursor.execute(sql.SQL("""
            INSERT INTO {} (member, connection_time)
            VALUES (%s, %s)
            """).format(sql.Identifier(room)), (username, datetime.datetime.now()))
            self.conn.commit()
            return True
        return False

    async def room_escape(self, username: str, room: str) -> bool:
        if await self.table_exist(room):
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

    async def table_exist(self, room):
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
