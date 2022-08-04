import jwt

from tests.src.config import Settings
from server.proto_api.server_proto_pb2 import AddFriendRequest, JoinRoomRequest, CreateRoomRequest, Message
from server.proto_api.server_proto_pb2_grpc import MessangerStub

USER = 'test_user'
PASSWD = 'passwd'
USER_2 = 'test_user_2'
USER_3 = 'test_user_3'
ROOM = 'test_room_1'
LOG_ROOM = 'r_test_room_1'
BAD_JWT = 'bad_jwt_format'
BAD_ROOM = 'bad_room'
ROOM_2 = 'test_room_2'


def jwt_encoder(username: str) -> bytes:
    key = Settings()
    key = key.secret_key
    _token = jwt.encode({"user": username}, key, algorithm="HS256")
    return _token


TOKEN_USER_2 = jwt_encoder(USER_2)
TOKEN = jwt_encoder(USER)
BAD_TOKEN = jwt_encoder('wrong_username')


def generate_friend(stub: MessangerStub):

    for user in (USER_3, USER_2):
        stub.AddFriend(
            AddFriendRequest(
                credentials=TOKEN,
                friend=user
            )
        )


def generate_rooms(stub: MessangerStub):

    for room in (ROOM, ROOM_2):
        stub.CreateRoom(
            CreateRoomRequest(
                credentials=TOKEN, room=room
            )
        )


def join_rooms(stub: MessangerStub):

    for room in (ROOM, ROOM_2):
        stub.JoinRoom(
            JoinRoomRequest(
                credentials=TOKEN,
                room=room
            )
        )


def generate_messages_for_room(stub: MessangerStub):
    generate_rooms(stub)
    number = 0
    for _ in range(5):
        message_ = f'hello_{number}'
        stub.SendMessage(
            Message(
                credentials=TOKEN,
                addressee=LOG_ROOM,
                message=message_
            )
        )
        number += 1


def generate_messages_for_friend(stub: MessangerStub):
    number = 0
    for _ in range(5):
        message = f'hello_{number}'
        stub.SendMessage(
            Message(
                credentials=TOKEN,
                addressee=USER_2,
                message=message
            )
        )
        number += 1
