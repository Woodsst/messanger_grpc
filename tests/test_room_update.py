import json

from server.proto_api.server_proto_pb2 import RequestSelfInfo
from tests.src.client_data_for_tests import TOKEN, generate_messages_for_room, ROOM


def test_client_get_update_room(send_message, orm):
    generate_messages_for_room(send_message)

    response = send_message.UpdateFriend(
        UpdateMessagesReqeuest(credentials=TOKEN,
                               time=1655105727,
                               update=ROOM
                               )
    )

    response = json.loads(response.json_info)
    assert len(response['rooms_update']['log_r_test_room_1']) == 5
