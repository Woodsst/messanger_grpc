import json

import jwt
from server.config import Settings
from server.orm import Orm


def credentials_validation(credentials: str) -> str or bool:
    key = Settings()
    key = key.secret_key
    try:
        _decode = jwt.decode(jwt=credentials, key=key, algorithms="HS256")
    except jwt.exceptions.DecodeError:
        return False
    return _decode


async def get_client_info(credentials: str, db: Orm) -> dict or bool:
    client = credentials_validation(credentials)
    if client is not False:
        information = await db.get_client_information(client['user'])
        if information is False:
            return False
        return json.loads(information)
    return False


