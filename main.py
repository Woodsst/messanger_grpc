import asyncio

from server.server import server_run
from server.orm import Orm
from server.logging_config import logger_config
from server.config import Settings

import logging

logger = logging.getLogger()


async def main():
    logger_config()
    config = Settings()
    orm = Orm(config)
    await orm.connect()
    logger.info("i'm born")
    await server_run(orm)


if __name__ == '__main__':
    asyncio.run(main())
