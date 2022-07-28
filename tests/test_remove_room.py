from tests.client_data_for_tests import TOKEN, ROOM, ROOM_2
from server.proto_api.server_proto_pb2 import RemoveRoomReqeust, CreateRoomRequest


def test_remove_room(send_message, orm):
    send_message.CreateRoom(
        CreateRoomRequest(room=ROOM, credentials=TOKEN)
    )

    response = send_message.RemoveRoom(
        RemoveRoomReqeust(
            room=ROOM,
            credentials=TOKEN
        )
    )
    assert response.status == 1


def test_remove_room_error(send_message, orm):
    send_message.CreateRoom(
        CreateRoomRequest(room=ROOM, credentials=TOKEN)
    )

    response = send_message.RemoveRoom(
        RemoveRoomReqeust(
            room=ROOM_2,
            credentials=TOKEN
        )
    )
    assert response.status == 2
