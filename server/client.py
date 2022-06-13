import json

from server.orm import Orm
from server.server_proto_pb2 import Response, CodeResult, ClientInfo


class Client:
    def __init__(self, name: str, orm: Orm = None):
        self.name = name
        self.orm = orm

    async def send_message(self, message: str, addressee: str) -> Response:
        if addressee[:2] == 'r_':
            if await self.orm.message_in_room(message, addressee, self.name):
                return Response(status=CodeResult.Value('ok'))
            return Response(status=CodeResult.Value('bad'))

        if await self.orm.message_for_friend(message, addressee, self.name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def add_friend(self, friend_name: str) -> Response:
        if await self.orm.add_friend(self.name, friend_name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def join_room(self, room: str) -> Response:
        room = f'r_{room}'
        if await self.orm.join_room(self.name, room):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def create_room(self, room_name: str) -> Response:
        if len(room_name) <= 0:
            return Response(status=CodeResult.Value('bad'))

        room_name = f'r_{room_name}'
        if await self.orm.add_new_room(room_name, self.name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def remove_friend(self, friend_name: str) -> Response:
        if await self.orm.remove_friend(friend_name, self.name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def room_escape(self, room: str) -> Response:
        room = f'r_{room}'
        if await self.orm.room_escape(self.name, room):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def get_messages_update(self, time: int) -> dict:
        info = await self.orm.get_client_information(self.name)
        info = json.loads(info)
        friends_update = await self.orm.update_friend_logs(self.name, info['friend_list'], time)
        rooms_update = await self.orm.update_room_logs(info['room_list'], time)
        updates = {"friends_update": friends_update,
                   "rooms_update": rooms_update,
                   "info": info}
        return ClientInfo(status=CodeResult.Value('ok'),
                          json_info=json.dumps(updates))

