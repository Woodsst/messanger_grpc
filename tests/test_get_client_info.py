import json
import time

from tests.src.client_data_for_tests import TOKEN, join_rooms, USER, BAD_TOKEN, BAD_JWT, generate_friend
from server.proto_api.server_proto_pb2 import RequestSelfInfo


def test_get_client_info(send_message, orm):

    generate_friend(send_message)
    join_rooms(send_message)

    response = send_message.InformationRequest(
        RequestSelfInfo(credentials=TOKEN, time=int(time.time())))

    assert response.status == 1
    response = json.loads(response.json_info)

    assert len(response) == 3
    assert response['username'] == USER
    assert len(response['friend_list']) == 2
    assert len(response['room_list']) == 2


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

