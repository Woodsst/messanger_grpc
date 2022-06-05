import jwt

from config import Settings

USER = 'test_user'
PASSWD = 'passwd'
USER_2 = 'test_user_2'
USER_3 = 'test_user_3'
ROOM = 'test_room'
BAD_JWT = 'bad_jwt_format'
BAD_ROOM = 'bad_room'


def jwt_encoder(username: str) -> bytes:
    key = Settings()
    key = key.secret_key
    _token = jwt.encode({"user": username}, key, algorithm="HS256")
    return _token


TOKEN = jwt_encoder(USER)
BAD_TOKEN = jwt_encoder('wrong_username')


