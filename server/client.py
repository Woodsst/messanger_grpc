from server.orm import Orm


class Client:
    def __init__(self, name: str, orm: Orm = None):
        self.name = name
        self.orm = orm

    def my_room(self) -> list:
        """
        Request in DB for return list rooms
        :return: list
        """
        pass

    def my_friends(self) -> list:
        """
        Request in DB for return list friends
        :return: list
        """
        pass

    async def add_friend(self, friend_name: str) -> bool:
        """
        Send friendship offer
        :param friend_name: string
        :return:
        """
        if await self.orm.add_friend(self.name, friend_name):
            return True
        return False

    async def join_room(self, room: str):
        """
        Connection to existing room
        :param room: class Room
        :return:
        """
        room = f'r_{room}'
        if await self.orm.join_room(self.name, room):
            return True
        return False

    async def create_room(self, room_name: str):
        """
        Creating custom room
        :param room_name: uniq room name
        :return:
        """
        room_name = f'r_{room_name}'
        if await self.orm.add_new_room(room_name, self.name):
            return True
        return False

    def send_message(self, message: str, room_name: str = None, other_client=None):
        """
        Send message in room or friend
        :param other_client: sting
        :param room_name: string
        :param message: string message
        :return:
        """
        pass

    async def remove_friend(self, friend_name: str) -> bool:
        """
        Remove friend from friend list
        :param friend_name: string
        :return: bool
        """
        if await self.orm.remove_friend(friend_name, self.name):
            return True
        return False

    async def room_escape(self, room: str) -> bool:
        """
        unjoin room
        :param room: string
        :return: bool
        """
        room = f'r_{room}'
        if await self.orm.room_escape(room, self.name):
            return True
        return False
