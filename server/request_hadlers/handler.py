import enum

import server.proto_api.server_proto_pb2 as api
from server.request_hadlers.client import Client
from server.request_hadlers.credentials import get_client_info
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
    """Request handler"""

    def __init__(self, orm: Orm):
        self.orm = orm

    async def handle(self, request, request_type: str) -> api.Response:
        """Handler all requests from clients"""

        client = await self.check_client(request.credentials)
        if client is False:
            return api.Response(status=api.CodeResult.Value('bad'))

        elif request_type == Requests.SEND_MESSAGE:
            return await client.send_message(request.message, request.addressee)

        elif request_type == Requests.INFORMATION_REQUEST:
            return await client.get_messages_update(request.time)

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
        """Checking client existence"""

        info = await get_client_info(credentials, self.orm)
        if info:
            client = Client(info['username'], self.orm)
            return client
        return False
