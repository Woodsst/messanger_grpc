import asyncio

from server.server import server_run
from server.orm import Orm
from server.logging_config import logger_config
from server.config import Settings

import logging

logger = logging.getLogger()

if __name__ == '__main__':
    logger_config()
    config = Settings()
    orm = Orm(config)
    logger.info("i'm born")
    asyncio.run(server_run(orm))
