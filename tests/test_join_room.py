from client_data_for_tests import TOKEN, BAD_TOKEN, ROOM, BAD_ROOM
from server_proto_pb2 import JoinRoomRequest, Response


def test_join_room(send_message, orm):
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
