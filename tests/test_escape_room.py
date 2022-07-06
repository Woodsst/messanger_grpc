from client_data_for_tests import TOKEN, BAD_TOKEN, ROOM
from proto_api.server_proto_pb2 import EscapeRoomRequest, JoinRoomRequest, CreateRoomRequest


def test_escape_room(send_message, orm):
    send_message.CreateRoom(
        CreateRoomRequest(credentials=TOKEN, room=ROOM)
    )
    send_message.JoinRoom(
        JoinRoomRequest(credentials=TOKEN, room=ROOM))
    response = send_message.RoomEscape(
        EscapeRoomRequest(credentials=TOKEN, room=ROOM)
    )
    assert response.status == 1


def test_escape_room_error(send_message, orm):
    response = send_message.RoomEscape(
        EscapeRoomRequest(credentials=BAD_TOKEN, room=ROOM)
    )
    assert response.status == 2
    response = send_message.RoomEscape(
        EscapeRoomRequest(credentials=TOKEN, room='')
    )
    assert response.status == 2
