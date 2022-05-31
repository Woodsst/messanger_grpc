from client_data_for_tests import TOKEN, USER, BAD_TOKEN
from server_proto_pb2 import RequestSelfInfo
import json


def test_get_client_info(server_start, send_message, orm):
    response = send_message.InformationRequest(
        RequestSelfInfo(credentials=TOKEN))
    assert response.status == 1
    response = json.loads(response.json_info)
    assert len(response) == 3
    assert response['username'] == USER
    assert len(response['friend_list']) == 2
    assert len(response['room_list']) == 2


def test_get_client_info_bad_request(send_message):
    response = send_message.InformationRequest(
        RequestSelfInfo(credentials=BAD_TOKEN))
    assert response.status == 2
    response = send_message.InformationRequest(
        RequestSelfInfo(credentials='not_jwt_format')
    )
    assert response.status == 2
    response = send_message.InformationRequest(
        RequestSelfInfo(credentials='')
    )
    assert response.status == 2
