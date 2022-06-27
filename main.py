import asyncio

from server.server import server_run
from server.orm import Orm
from server.logging_config import logger
from server.config import Settings


async def main():
    config = Settings()
    orm = Orm(config)
    await orm.connect()
    logger.info("server for messanger start")
    await server_run(orm)


if __name__ == '__main__':
    asyncio.run(main())
