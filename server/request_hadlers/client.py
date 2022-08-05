import json

from server.orm import Orm
from server.proto_api.server_proto_pb2 import Response, CodeResult, ClientInfo, UpdateData


class Client:
    def __init__(self, name: str, orm: Orm = None):
        self.name = name
        self.orm = orm

    async def remove_room(self, room_name: str) -> Response:
        """Request to the database to delete the client room"""

        room_name = f'r_{room_name}'
        if await self.orm.remove_room(room_name, self.name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def send_message(self, message: str, addressee: str) -> Response:
        """Request to the database to send message"""

        if addressee[:2] == 'r_':  # 'r_' - indicates that the addressee is a group
            if await self.orm.message_in_room(message, addressee, self.name):
                return Response(status=CodeResult.Value('ok'))
            return Response(status=CodeResult.Value('bad'))

        if await self.orm.message_for_friend(message, addressee, self.name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def add_friend(self, friend_name: str) -> Response:
        """Request to the database to add friend"""

        if await self.orm.add_friend(self.name, friend_name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def join_room(self, room: str) -> Response:
        """Request to the database to join the room"""

        room = f'r_{room}'
        if await self.orm.join_room(self.name, room):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def create_room(self, room_name: str) -> Response:
        """Request to the database to create new room"""

        if len(room_name) <= 0:
            return Response(status=CodeResult.Value('bad'))

        room_name = f'r_{room_name}'  # 'r_' is needed to define a table as a room
        if await self.orm.add_new_room(room_name, self.name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def remove_friend(self, friend_name: str) -> Response:
        """Request to the database to remove friend"""

        if await self.orm.remove_friend(friend_name, self.name):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def room_escape(self, room: str) -> Response:
        """Request to the database to leave from the room"""

        room = f'r_{room}'
        if await self.orm.room_escape(self.name, room):
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def get_client_info_update(self) -> ClientInfo:
        """Returning an update in customer information"""

        info = await self.orm.get_client_information(self.name)
        info = json.loads(info)
        return ClientInfo(status=CodeResult.Value('ok'),
                          json_info=json.dumps(info))

    async def messages_update(self, update: str, update_time: int) -> UpdateData:
        """Handler for returning new messages"""

        if update[:2] == 'r_':
            update = f'log_{update}'
            update = await self.orm.check_update_in_log(update, update_time)
            return UpdateData(status=CodeResult.Value('ok'),
                              json_info=json.dumps([dict(record) for record in update]))

        log_name = await self.orm.check_friend_log_exist(update, self.name)
        update = await self.orm.check_update_in_log(log_name, update_time)

        return UpdateData(status=CodeResult.Value('ok'),
                          json_info=json.dumps([dict(record) for record in update]))
