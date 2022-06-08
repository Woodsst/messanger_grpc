from client_data_for_tests import USER_2, TOKEN, ROOM, LOG_ROOM, BAD_TOKEN
from server_proto_pb2 import Message, CreateRoomRequest


def test_send_message_in_room(send_message, orm):
    send_message.CreateRoom(CreateRoomRequest(credentials=TOKEN, room=ROOM))
    response = send_message.SendMessage(
        Message(message='hello', addressee=LOG_ROOM, credentials=TOKEN))
    assert response.status == 1


def test_send_message_in_room_error(send_message, orm):
    send_message.CreateRoom(CreateRoomRequest(credentials=TOKEN, room=ROOM))
    response = send_message.SendMessage(
        Message(message='hello', addressee=LOG_ROOM, credentials=BAD_TOKEN))
    assert response.status == 2
    response = send_message.SendMessage(
        Message(message='hello', addressee='unexist_room', credentials=BAD_TOKEN))
    assert response.status == 2


def test_send_message_for_friend(send_message, orm):
    pass


def test_send_message_for_friend_error(send_message, orm):
    pass
