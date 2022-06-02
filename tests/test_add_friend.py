from client_data_for_tests import TOKEN, BAD_TOKEN, USER_3, USER_2
from server_proto_pb2 import FriendRequest


def test_add_friend(server_start, send_message, orm):
    response = send_message.AddFriend(
        FriendRequest(friend=USER_3, credentials=TOKEN))
    assert response.status == 1


def test_add_friend_error(send_message, orm):
    response = send_message.AddFriend(
        FriendRequest(credentials=BAD_TOKEN))
    assert response.status == 2
    response = send_message.AddFriend(
        FriendRequest(credentials=TOKEN, friend='unexist_user')
    )
    assert response.status == 2
    response = send_message.AddFriend(
        FriendRequest(credentials=TOKEN, friend=USER_2)
    )
    assert response.status == 2