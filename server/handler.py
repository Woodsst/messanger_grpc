import enum

import server.server_proto_pb2 as api
from server.client import Client
from server.credentials import get_client_info
from server.orm import Orm


class Requests(enum.Enum):
    SEND_MESSAGE = "Send message"
    INFORMATION_REQUEST = "Information request"
    CREATE_ROOM = "Create room"
    JOIN_ROOM = "Join room"
    ROOM_ESCAPE = "Room escape"
    ADD_FRIEND = "Add friend"
    REMOVE_FRIEND = "Remove friend"


class RequestHandler:
    def __init__(self, orm: Orm):
        self.orm = orm

    async def handle(self, request, request_type: str) -> api.Response:
        client = await self.check_client(request.credentials)
        if client is False:
            return api.Response(status=api.CodeResult.Value('bad'))

        if request_type == Requests.SEND_MESSAGE:
            return await client.send_message(request.message, request.addressee)

        requests = {
            Requests.CREATE_ROOM: client.create_room,
            Requests.ADD_FRIEND: client.add_friend,
            Requests.REMOVE_FRIEND: client.remove_friend,
            Requests.JOIN_ROOM: client.join_room,
            Requests.ROOM_ESCAPE: client.room_escape,
        }

        try:
            return await requests[request_type](request.friend)
        except AttributeError:
            return await requests[request_type](request.room)

    async def check_client(self, credentials: str) -> Client or bool:
        info = await get_client_info(credentials, self.orm)
        if info:
            client = Client(info['username'], self.orm)
            return client
        return False
