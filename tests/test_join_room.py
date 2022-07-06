from client_data_for_tests import TOKEN, BAD_TOKEN, ROOM, BAD_ROOM
from proto_api.server_proto_pb2 import JoinRoomRequest, Response, CreateRoomRequest


def test_join_room(send_message, orm):
    send_message.CreateRoom(
        CreateRoomRequest(credentials=TOKEN, room=ROOM)
    )
    response = send_message.JoinRoom(
        JoinRoomRequest(credentials=TOKEN, room=ROOM)
    )
    assert response.status == 1
    assert isinstance(response, Response)


def test_join_room_error(send_message, orm):
    response = send_message.JoinRoom(
        JoinRoomRequest(credentials=BAD_TOKEN, room=ROOM)
    )
    assert response.status == 2
    response = send_message.JoinRoom(
        JoinRoomRequest(credentials=TOKEN, room=BAD_ROOM)
    )
    assert response.status == 2

