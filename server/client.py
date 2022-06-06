from server.orm import Orm


class Client:
    def __init__(self, name: str, orm: Orm = None):
        self.name = name
        self.orm = orm

    def my_room(self) -> list:
        pass

    def my_friends(self) -> list:
        pass

    async def add_friend(self, friend_name: str) -> bool:
        if await self.orm.add_friend(self.name, friend_name):
            return True
        return False

    async def join_room(self, room: str):
        room = f'r_{room}'
        if await self.orm.join_room(self.name, room):
            return True
        return False

    async def create_room(self, room_name: str) -> bool:
        if len(room_name) <= 0:
            return False

        room_name = f'r_{room_name}'
        if await self.orm.add_new_room(room_name, self.name):
            return True

        return False

    def send_message(self, message: str, room_name: str = None, other_client=None):
        pass

    async def remove_friend(self, friend_name: str) -> bool:
        if await self.orm.remove_friend(friend_name, self.name):
            return True
        return False

    async def room_escape(self, room: str) -> bool:
        room = f'r_{room}'
        if await self.orm.room_escape(self.name, room):
            return True
        return False
