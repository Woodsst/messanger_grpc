import jwt

from tests.src.config import Settings
from server.proto_api.server_proto_pb2 import AddFriendRequest, JoinRoomRequest
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


def join_rooms(stub: MessangerStub):

    for room in (ROOM, ROOM_2):
        stub.JoinRoom(
            JoinRoomRequest(
                credentials=TOKEN,
                room=room
            )
        )
