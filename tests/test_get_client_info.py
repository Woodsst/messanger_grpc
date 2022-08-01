import json
import time

from tests.src.client_data_for_tests import TOKEN, join_rooms, USER, BAD_TOKEN, BAD_JWT, LOG_ROOM, ROOM, USER_2, generate_friend
from server.proto_api.server_proto_pb2 import RequestSelfInfo, Message, CreateRoomRequest


def test_get_client_info(send_message, orm):

    generate_friend(send_message)
    join_rooms(send_message)

    response = send_message.InformationRequest(
        RequestSelfInfo(credentials=TOKEN, time=int(time.time())))

    assert response.status == 1
    response = json.loads(response.json_info)

    assert len(response) == 3
    assert response['info']['username'] == USER
    assert len(response['info']['friend_list']) == 2
    assert len(response['info']['room_list']) == 2


def test_get_client_info_bad_request(send_message):
    response = send_message.InformationRequest(
        RequestSelfInfo(credentials=BAD_TOKEN, time=int(time.time())))
    assert response.status == 2
    response = send_message.InformationRequest(
        RequestSelfInfo(credentials=BAD_JWT, time=int(time.time()))
    )
    assert response.status == 2
    response = send_message.InformationRequest(
        RequestSelfInfo(credentials='', time=int(time.time()))
    )
    assert response.status == 2


def test_client_get_update_room(send_message, orm):
    send_message.CreateRoom(CreateRoomRequest(
        credentials=TOKEN, room=ROOM
    ))
    number = 0
    for _ in range(5):
        message_ = f'hello_{number}'
        send_message.SendMessage(
            Message(
                credentials=TOKEN,
                addressee=LOG_ROOM,
                message=message_
            )
        )
        number += 1
    for _ in range(5):
        message_ = f'hello_{number}'
        send_message.SendMessage(
            Message(
                credentials=TOKEN,
                addressee=USER_2,
                message=message_
            )
        )
        number += 1
    response = send_message.InformationRequest(
        RequestSelfInfo(credentials=TOKEN,
                        time=1655105727
                        )
    )
    response = json.loads(response.json_info)
    assert len(response['friends_update']['test_user_2']) == 5
    assert len(response['rooms_update']['log_r_test_room_1']) == 5
