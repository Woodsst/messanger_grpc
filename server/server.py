import grpc

from server.handler import RequestHandler, Requests
from server.orm import Orm
from server.server_proto_pb2 import ClientInfo, Response
from server.server_proto_pb2_grpc import MessangerServicer, add_MessangerServicer_to_server


class Greeter(MessangerServicer):
    """A class that receives requests for processing from clients"""

    def __init__(self, orm: Orm):
        self.orm = orm
        self.handler = RequestHandler(self.orm)

    async def SendMessage(self, request, context) -> Response:
        """Handler of a request to sending a message to a client or room"""
        return await self.handler.handle(request, Requests.SEND_MESSAGE)

    async def InformationRequest(self, request, context) -> ClientInfo:
        """Handler of a request to update client information"""
        return await self.handler.handle(request, Requests.INFORMATION_REQUEST)

    async def CreateRoom(self, request, context) -> Response:
        """Handler of a request to create new room"""
        return await self.handler.handle(request, Requests.CREATE_ROOM)

    async def JoinRoom(self, request, context):
        """Handler of a request to join the room"""
        return await self.handler.handle(request, Requests.JOIN_ROOM)

    async def RoomEscape(self, request, context):
        """Handler of a request to leave the room"""
        return await self.handler.handle(request, Requests.ROOM_ESCAPE)

    async def AddFriend(self, request, context) -> Response:
        """Handler of a request to add a friend"""
        return await self.handler.handle(request, Requests.ADD_FRIEND)

    async def RemoveFriend(self, request, context) -> Response:
        """Handler of a request to remove a friend"""
        return await self.handler.handle(request, Requests.REMOVE_FRIEND)


async def server_run(server_address: str, orm: Orm):
    """starting grpc server"""

    server = grpc.aio.server()
    add_MessangerServicer_to_server(Greeter(orm), server)
    server.add_insecure_port(server_address)
    await server.start()
    await server.wait_for_termination()
