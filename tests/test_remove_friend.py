from client_data_for_tests import USER_2, TOKEN, BAD_TOKEN
from proto_api.server_proto_pb2 import RemoveFriendRequest


def test_remove_friend(send_message, orm):
    response = send_message.RemoveFriend(
        RemoveFriendRequest(friend=USER_2, credentials=TOKEN))
    assert response.status == 1


def test_remove_friend_error(send_message, orm):
    response = send_message.RemoveFriend(
        RemoveFriendRequest(friend=USER_2, credentials=BAD_TOKEN))
    assert response.status == 2
    response = send_message.RemoveFriend(
        RemoveFriendRequest(credentials=TOKEN, friend='unexist_user')
    )
    assert response.status == 2
    send_message.RemoveFriend(RemoveFriendRequest(credentials=TOKEN, friend=USER_2))
    response = send_message.RemoveFriend(
        RemoveFriendRequest(credentials=TOKEN, friend=USER_2)
    )
    assert response.status == 2
