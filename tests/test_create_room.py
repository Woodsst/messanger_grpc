from tests.src.client_data_for_tests import TOKEN, ROOM, BAD_TOKEN
from server.proto_api.server_proto_pb2 import CreateRoomRequest


def test_create_room(send_message, orm):
    response = send_message.CreateRoom(
        CreateRoomRequest(room=ROOM, credentials=TOKEN)
    )
    assert response.status == 1


def test_create_room_error(send_message, orm):
    response = send_message.CreateRoom(
        CreateRoomRequest(room=ROOM, credentials=BAD_TOKEN)
    )
    assert response.status == 2
    response = send_message.CreateRoom(
        CreateRoomRequest(room='', credentials=TOKEN)
    )
    assert response.status == 2
