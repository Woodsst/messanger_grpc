from server_proto_pb2 import Message
from client_data_for_tests import OTHER_USER, TOKEN, ROOM


def test_send_message_for_friend(send_message, orm):
    response = send_message.SendMessage(
        Message(message='hello', other_client=OTHER_USER, credentials=TOKEN))
    print(response)


def test_send_message_for_friend_error(send_message, orm):
    pass


def test_send_message_in_room(send_message, orm):
    response = send_message.SendMessage(
        Message(message='hello', room_name=ROOM, credentials=TOKEN))
    print(response)


def test_send_message_in_room_error(send_message, orm):
    pass
