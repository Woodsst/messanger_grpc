from server.orm import Orm
from server.server_proto_pb2 import Response, CodeResult


class Client:
    def __init__(self, name: str, orm: Orm = None):
        self.name = name
        self.orm = orm

    def send_message(self, message: str, room_name: str = None, other_client=None):
        pass

    async def add_friend(self, friend_name: str) -> Response:
        if await self.orm.add_friend(self.name, friend_name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def join_room(self, room: str) -> Response:
        room = f'r_{room}'
        if await self.orm.join_room(self.name, room):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def create_room(self, room_name: str) -> bool:
        if len(room_name) <= 0:
            return Response(status=CodeResult.Value('bad'))

        room_name = f'r_{room_name}'
        if await self.orm.add_new_room(room_name, self.name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def remove_friend(self, friend_name: str) -> bool:
        if await self.orm.remove_friend(friend_name, self.name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def room_escape(self, room: str) -> bool:
        room = f'r_{room}'
        if await self.orm.room_escape(self.name, room):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))
