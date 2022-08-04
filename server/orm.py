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
    """Class for connect PostgreSQL and use SQL-requests"""

    def __init__(self, config: Settings):
        self.config = config
        self.con: Union[Connection, None] = None

    async def connect(self):
        """connecting with database"""

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

    async def remove_room(self, room_name: str, username: str) -> bool:
        """SQL-request to remove a room"""

        if await self.room_exist(room_name) and await self.check_creator_room(username, room_name):
            room_log = f'log_{room_name}'
            async with self.con.transaction():
                await self.con.execute("""
                    DROP TABLE {};
                    DROP TABLE {};
                    """.format(room_name, room_log))
                return True
        return False

    async def check_creator_room(self, username: str, room_name: str) -> bool:
        """SQL-request that the client is the creator of the room"""

        result = await self.con.fetch("""
        SELECT creator
        FROM {}
        WHERE creator=$1
        """.format(room_name), username)

        if len(result) > 0:
            return True
        return False

    async def room_exist(self, room_name: str) -> bool:
        """SQL-request to check room exist"""

        result = await self.con.fetch("""
        SELECT * 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME=$1
        """, room_name)

        if len(result) > 0:
            return True
        return False

    async def check_update_in_log(self, log_name: str, update_time: int):
        """SQL-reqeust for updates in log table"""

        result = await self.con.fetch("""
        SELECT member, message, message_time
        FROM {0}
        WHERE message_time > $1
        """.format(log_name), update_time)
        if len(result) > 0:
            return result
        return []

    async def message_in_room(self, message: str, addressee: str, user: str) -> bool:
        """SQL-request for write a message to the room log"""

        if await self.table_exist(addressee) and await self.check_room_in_room_list(user, addressee):
            addressee = f'log_{addressee}'
            await self.con.execute("""
            INSERT INTO {0} (member, message, message_time)
            VALUES ($1, $2, $3)
            """.format(addressee), user, message, int(time.time()))
            return True
        return False

    async def check_room_in_room_list(self, username: str, room_name: str) -> bool:
        """SQL-request for checking the availability of a room in the client's room list"""

        result = await self.con.fetch("""
        SELECT client_group
        FROM clients_groups
        WHERE username=$1
        """, username)
        room_list = [x.get('client_group') for x in result]
        if room_name in room_list:
            return True
        return False

    async def message_for_friend(self, message: str, addressee: str, username: str) -> bool:
        """SQL-request for write a message to the friend log"""

        if await self.check_friend_in_friend_list(addressee, username):
            log_name = await self.create_log_friend_chat(addressee, username)
            await self.con.execute("""
            INSERT INTO {} (member, message, message_time)
            VALUES ($1, $2, $3)
            """.format(log_name), username, message, int(time.time()))
            return True
        return False

    async def check_friend_log_exist(self, addressee: str, username: str) -> str or bool:
        """Checking exist a friend log
        The friends' journal is created based on their names,
        so there are two possible variants of the journal name"""

        first = f'log_{addressee}_{username}'.lower()
        second = f'log_{username}_{addressee}'.lower()
        if await self.table_exist(first):
            return first
        if await self.table_exist(second):
            return second
        return False

    async def create_log_friend_chat(self, addressee: str, username: str) -> str:
        """Create table for friend chat"""

        log_name = await self.check_friend_log_exist(addressee, username)
        if log_name is False:
            log_name = f'{addressee}_{username}'
            await self.create_log_for_room(log_name)
            return f'log_{log_name}'
        return log_name

    async def get_client_information(self, name: str) -> dict or bool:
        """SQL-request for getting information about the client"""

        result = await self.con.fetch("""
        SELECT clients.username, client_friend, client_group
        FROM clients
        LEFT JOIN clients_friends ON clients.username = clients_friends.username
        LEFT JOIN clients_groups ON clients.username = clients_groups.username
        WHERE clients.username=$1;
        """, name)
        if len(result) == 0:
            return False
        information = self.data_to_dict(result)
        return information

    async def create_log_for_room(self, room: str):
        """SQL-request to create log the room"""

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
        """SQL-request to create a new room"""

        async with self.con.transaction():
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

            await self.add_room_in_room_list(room_name, creator)
            await self.add_creator_in_room(room_name, creator)
            await self.create_log_for_room(room_name)
            return True

    async def add_room_in_room_list(self, room_name: str, creator: str):
        """SQL-request to add room in creator room list"""

        await self.con.execute("""
            INSERT INTO clients_groups 
            (username, client_group)
            VALUES
            ($2, $1)
            """, room_name, creator)

    async def add_creator_in_room(self, room_name: str, creator: str):
        """SQL-request for add room creator"""

        await self.con.execute("""
        INSERT INTO {} (creator, member, connection_time)
        VALUES ($1, $2, $3)
        """.format(room_name), creator, creator, datetime.datetime.now())

    async def add_friend(self, user_name: str, friend_name: str) -> bool:
        """SQL-request to add a friend"""

        async with self.con.transaction():
            if await self.check_friend(friend_name, user_name):
                await self.append_in_friend_list(user_name, friend_name)
                await self.append_in_friend_list(friend_name, user_name)
                return True
            return False

    async def append_in_friend_list(self, user_name: str, friend_name: str):
        """SQL-request to append a friend to the friend list"""

        await self.con.execute("""
        INSERT INTO clients_friends 
        (username, client_friend)
        VALUES 
        ($2, $1)
        """, friend_name, user_name)

    async def check_friend_in_friend_list(self, friend_name: str, user_name: str) -> bool:
        """SQL-request to check if a friend is in the friends list"""

        result = await self.con.fetch("""
        SELECT client_friend
        FROM clients_friends
        WHERE username=$1
        """, user_name)
        friend_list = [x.get('client_friend') for x in result]
        if friend_name in friend_list:
            return True
        return False

    async def client_exist(self, user_name: str) -> bool:
        """SQL-request to verify the existence of a client"""

        result = await self.con.fetch("""
        SELECT username
        FROM clients
        WHERE username=$1
        """, user_name)
        if len(result) == 0:
            return False
        return True

    async def remove_friend(self, friend_name: str, user_name: str) -> bool:
        """SQL-request to remove friend from the friend list"""

        if not await self.client_exist(friend_name):
            return False
        elif not await self.check_friend_in_friend_list(friend_name, user_name):
            return False
        await self.con.execute("""
            DELETE FROM clients_friends
            WHERE username = $2 AND  client_friend = $1
            """, friend_name, user_name)
        return True

    async def check_friend(self, friend_name: str, user_name: str) -> bool:
        """Check the friend in client list and friend list"""

        if not await self.client_exist(friend_name):
            return False
        elif await self.check_friend_in_friend_list(friend_name, user_name):
            return False
        return True

    async def join_room(self, username: str, room: str) -> bool:
        """SQL-request to join an existing room"""

        if await self.table_exist(room):
            await self.con.execute("""
            INSERT INTO {} (member, connection_time)
            VALUES ($1, $2)
            """.format(room), username, datetime.datetime.now())
            await self.add_room_in_room_list(room, username)
            return True
        return False

    async def room_escape(self, username: str, room: str) -> bool:
        """SQL-request to leave the room"""

        if await self.table_exist(room):
            await self.con.execute("""
            DELETE FROM {}
            WHERE member = $1
            """.format(room), username)
            await self.delete_room_from_room_list(username, room)
            return True
        return False

    async def delete_room_from_room_list(self, username: str, room: str):
        """SQL-request to remove a room from the list rooms"""

        await self.con.execute("""
        DELETE FROM clients_groups
        WHERE username = $2 AND client_group = $1
        """, room, username)

    async def table_exist(self, room):
        """SQL-request to check the existence of a table"""

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
        """Formatting tuple(Record) to dict for JSON dump"""

        friend_list = {friend.get('client_friend') for friend in data}
        if None in friend_list: friend_list.remove(None)

        room_list = {room.get('client_group') for room in data}
        if None in room_list: room_list.remove(None)

        result = {
            "username": data[0]['username'],
            "friend_list": tuple(friend_list),
            "room_list": tuple(room_list)
        }

        result = json.dumps(result)
        return result
