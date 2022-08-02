import json

from server.proto_api.server_proto_pb2 import MessagesUpdateRequest
from tests.src.client_data_for_tests import TOKEN, USER_2, generate_messages_for_friend, generate_friend


def test_client_get_update_room(send_message, orm):
    generate_friend(send_message)
    generate_messages_for_friend(send_message)

    response = send_message.MessagesUpdate(
        MessagesUpdateRequest(credentials=TOKEN,
                              time=1655105727,
                              update=USER_2
                              )
    )

    response = json.loads(response.json_info)
    assert len(response) == 5
