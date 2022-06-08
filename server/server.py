import json
import logging

import grpc

from server.credentials import get_client_info
from server.handler import RequestHandler, Requests
from server.orm import Orm
from server.server_proto_pb2 import ClientInfo, CodeResult, Response
from server.server_proto_pb2_grpc import add_GreeterServicer_to_server, GreeterServicer

logger = logging.getLogger()


class Greeter(GreeterServicer):
    def __init__(self, orm: Orm):
        self.orm = orm
        self.handler = RequestHandler(self.orm)

    async def SendMessage(self, request, context) -> Response:
        return await self.handler.handle(request, Requests.SEND_MESSAGE)

    async def InformationRequest(self, request, context) -> ClientInfo:
        info = await get_client_info(request.credentials, self.orm)
        if info:
            return ClientInfo(json_info=json.dumps(info),
                              status=CodeResult.Value('ok'))
        return ClientInfo(status=CodeResult.Value('bad'))

    async def CreateRoom(self, request, context) -> Response:
        return await self.handler.handle(request, Requests.CREATE_ROOM)

    async def JoinRoom(self, request, context):
        return await self.handler.handle(request, Requests.JOIN_ROOM)

    async def RoomEscape(self, request, context):
        return await self.handler.handle(request, Requests.ROOM_ESCAPE)

    async def AddFriend(self, request, context) -> Response:
        return await self.handler.handle(request, Requests.ADD_FRIEND)

    async def RemoveFriend(self, request, context) -> Response:
        return await self.handler.handle(request, Requests.REMOVE_FRIEND)


async def server_run(orm: Orm):
    server = grpc.aio.server()
    add_GreeterServicer_to_server(Greeter(orm), server)
    server.add_insecure_port('localhost:5000')
    await server.start()
    await server.wait_for_termination()
