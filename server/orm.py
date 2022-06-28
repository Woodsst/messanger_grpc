import asyncio
import datetime
import json
import time
from typing import Union

import asyncpg
import psycopg
from asyncpg import Connection
from server.logging_config import logger
from server.config import Settings


class Orm:
    def __init__(self, config: Settings):
        self.config = config
        self.con: Union[Connection, None] = None

    async def connect(self):
        timeout = 0.1
        connect = False
        while not connect:
            await asyncio.sleep(timeout)
            try:
                self.con = await asyncpg.connect(
                    database=self.config.db_name,
                    user=self.config.db_username,
                    password=self.config.db_password,
                    host=self.config.db_host,
                    port=self.config.db_port)
            except ConnectionRefusedError:
                timeout += 0.1
                if timeout > 0.5:
                    logger.critical('Error - connect to database host: %s, port: %s',
                                    self.config.db_host, self.config.db_port)
                    raise
                continue
            connect = True

    async def update_friend_logs(self, username: str, friend_list: list, update_time: int) -> dict:
        update_friend_messages = {}
        for friend in friend_list:
            log = await self.check_friend_log_exist(friend, username)
            if log:
                update = await self.check_update_in_log(log, update_time)
                if update is not False:
                    update = self.record_parce(update)
                    update_friend_messages[friend] = update
        return update_friend_messages

    async def update_room_logs(self, room_list: list, update_time: int) -> dict:
        update_room_messages = {}
        for room in room_list:
            room = f'log_{room}'
            if await self.table_exist(room):
                update = await self.check_update_in_log(room, update_time)
                update = self.record_parce(update)
                update_room_messages[room] = update
        return update_room_messages

    async def check_update_in_log(self, log_name: str, update_time: int):
        result = await self.con.fetch("""
        SELECT *
        FROM {}
        WHERE message_time > $1
        """.format(log_name), update_time)
        if len(result) > 0:
            return result
        return False

    async def message_in_room(self, message: str, addressee: str, user: str) -> bool:
        if await self.table_exist(addressee) and await self.check_room_in_room_list(user, addressee):
            addressee = f'log_{addressee}'
            await self.con.execute("""
            INSERT INTO {} (member, message, message_time)
            VALUES ($1, $2, $3)
            """.format(addressee), user, message, int(time.time()))
            return True
        return False

    async def check_room_in_room_list(self, username: str, room_name: str) -> bool:
        result = await self.con.fetch("""
        SELECT array_position(room_list, $1)
        FROM clients
        WHERE username=$2
        """, room_name, username)
        if result[0][0] is None:
            return False
        return True

    async def message_for_friend(self, message: str, addressee: str, username: str) -> bool:
        if await self.check_friend_in_friend_list(addressee, username):
            log_name = await self.create_log_friend_chat(addressee, username)
            await self.con.execute("""
            INSERT INTO {} (member, message, message_time)
            VALUES ($1, $2, $3)
            """.format(log_name), username, message, int(time.time()))
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
        result = await self.con.fetch("""
        SELECT username, friend_list, room_list
        FROM clients
        WHERE username=$1
        """, name)
        if len(result) == 0:
            return False
        information = self.data_to_dict(result)
        return information

    async def create_log_for_room(self, room: str):
        room = f'log_{room}'
        await self.con.execute("""
            CREATE TABLE IF NOT EXISTS {}
                (
                member varchar NOT null,
                message varchar,
                message_time int NOT null
                )
            """.format(room))

    async def add_new_room(self, room_name: str, creator: str) -> bool:
        try:
            await self.con.execute("""
            CREATE TABLE {}
            (
            creator varchar,
            member varchar NOT null,
            connection_time date NOT null
            )
            """.format(room_name))
        except psycopg.errors.DuplicateTable:
            return False

        await self.add_creator_in_room(room_name, creator)
        await self.create_log_for_room(room_name)
        return True

    async def add_creator_in_room(self, room_name: str, creator: str):
        await self.con.execute("""
        INSERT INTO {} (creator, member, connection_time)
        VALUES ($1, $2, $3)
        """.format(room_name), creator, creator, datetime.datetime.now())

    async def add_friend(self, user_name: str, friend_name: str) -> bool:
        if await self.check_friend(friend_name, user_name):
            await self.con.execute("""
            UPDATE clients
            SET friend_list = array_append(friend_list, $1)
            WHERE username = $2
            """, friend_name, user_name)
            return True
        return False

    async def check_friend_in_friend_list(self, friend_name: str, user_name: str) -> bool:
        result = await self.con.fetch("""
        SELECT array_position(friend_list, $1)
        FROM clients
        WHERE username=$2
        """, friend_name, user_name)
        if result[0][0] is None:
            return False
        return True

    async def client_exist(self, client_name: str) -> bool:
        result = await self.con.fetch("""
        SELECT username
        FROM clients
        WHERE username=$1
        """, client_name)
        if len(result) == 0:
            return False
        return True

    async def remove_friend(self, friend_name: str, user_name: str) -> bool:
        if not await self.client_exist(friend_name):
            return False
        elif not await self.check_friend_in_friend_list(friend_name, user_name):
            return False
        await self.con.execute("""
            UPDATE clients
            SET friend_list = array_remove(friend_list, $1)
            WHERE username = $2
            """, friend_name, user_name)
        return True

    async def check_friend(self, friend_name: str, user_name: str) -> bool:
        if not await self.client_exist(friend_name):
            return False
        elif await self.check_friend_in_friend_list(friend_name, user_name):
            return False
        return True

    async def join_room(self, username: str, room: str) -> bool:
        if await self.table_exist(room):
            await self.con.execute("""
            INSERT INTO {} (member, connection_time)
            VALUES ($1, $2)
            """.format(room), username, datetime.datetime.now())
            return True
        return False

    async def room_escape(self, username: str, room: str) -> bool:
        if await self.table_exist(room):
            await self.con.execute("""
            DELETE FROM {}
            WHERE member = $1
            """.format(room), username)
            await self.delete_room_from_room_list(username, room)
            return True
        return False

    async def delete_room_from_room_list(self, username: str, room: str):
        await self.con.execute("""
        UPDATE clients
        SET room_list = array_remove(room_list, $1)
        WHERE username = $2
        """, room, username)

    async def table_exist(self, room):
        result = await self.con.fetch("""
        SELECT EXISTS (
            SELECT FROM
                pg_tables
            WHERE
                schemaname = 'public' AND
                tablename  = $1
            )
        """, room)

        if result[0][0] is True:
            return True
        return False

    @staticmethod
    def data_to_dict(data: tuple) -> dict:

        result = {
            "username": data[0]['username'],
            "friend_list": data[0]['friend_list'],
            "room_list": data[0]['room_list']
        }

        result = json.dumps(result)
        return result

    @staticmethod
    def record_parce(record_list: list):
        result = []
        for i in record_list:
            result.append(dict(i))
        print(result)
        return result
