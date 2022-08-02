import json
from typing import Union

import jwt

from server.config import Settings
from server.logging_config import logger
from server.orm import Orm


def credentials_validation(credentials: str) -> Union[str, bool]:
    """Decode client jwt"""

    key = Settings()
    key = key.secret_key
    try:
        _decode = jwt.decode(jwt=credentials, key=key, algorithms="HS256")
    except jwt.exceptions.DecodeError:
        logger.exception('jwt exeption, credentials - %s' % credentials, exc_info=jwt.exceptions.DecodeError())
        return False
    return _decode


async def get_client_info(credentials: str, db: Orm) -> Union[dict, bool]:
    """Getting client information from the database"""

    client = credentials_validation(credentials)
    if client is not False:
        information = await db.get_client_information(client['user'])
        if information is False:
            logger.info('bad credentials - wrong username or pass')
            return False
        return json.loads(information)
    return False
