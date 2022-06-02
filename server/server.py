import json
import logging

import grpc

from server.client import Client
from server.credentials import get_client_info
from server.orm import Orm
from server.server_proto_pb2 import ClientInfo, CodeResult, Response
from server.server_proto_pb2_grpc import add_GreeterServicer_to_server, GreeterServicer

logger = logging.getLogger()


class Greeter(GreeterServicer):
    def __init__(self, orm: Orm):
        self.orm = orm

    async def SendMessage(self, request, context) -> Response:
        info = await get_client_info(request.credentials, self.orm)
        if info:
            client = Client(info['username'])
            if request.room_name:
                client.send_message(message=request.message, room_name=request.room_name)
            elif request.other_client:
                client.send_message(message=request.message, other_client=request.other_client)
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def InformationRequest(self, request, context) -> ClientInfo:
        info = await get_client_info(request.credentials, self.orm)
        if info:
            return ClientInfo(json_info=json.dumps(info), status=CodeResult.Value('ok'))
        else:
            return ClientInfo(status=CodeResult.Value('bad'))

    async def CreateRoom(self, request, context) -> Response:
        info = await get_client_info(request.credentials, self.orm)
        if info:
            client = Client(info['username'], self.orm)
            await client.create_room(request.room)
            return Response(status=CodeResult.Value('ok'))
        return Response(status=CodeResult.Value('bad'))

    async def EnterRoom(self, request, context):
        pass

    async def EscapeOutRoom(self, request, context):
        pass

    async def AddFriend(self, request, context) -> Response:
        info = await get_client_info(request.credentials, self.orm)
        if info:
            client = Client(info['username'], self.orm)
            if await client.add_friend(request.friend):
                return Response(status=CodeResult.Value('ok'))
            return Response(status=CodeResult.Value('bad'))
        return Response(status=CodeResult.Value('bad'))

    async def DeleteFriend(self, request, context) -> Response:
        info = await get_client_info(request.credentials, self.orm)
        if info:
            client = Client(info['username'], self.orm)
            if await client.remove_friend(request.friend):
                return Response(status=CodeResult.Value('ok'))
            return Response(status=CodeResult.Value('bad'))
        return Response(status=CodeResult.Value('bad'))


async def server_run(orm: Orm):
    server = grpc.aio.server()
    add_GreeterServicer_to_server(Greeter(orm), server)
    server.add_insecure_port('localhost:5000')
    await server.start()
    await server.wait_for_termination()
