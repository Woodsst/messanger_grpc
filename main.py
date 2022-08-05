import asyncio
import asyncpg

from server.server import server_run
from server.orm import Orm
from server.logging_config import logger
from server.config import Settings


async def pool_sql(config: Settings) -> asyncpg.Pool:
    pool = await asyncpg.create_pool(
        host=config.db_host,
        port=config.db_port,
        user=config.db_username,
        password=config.db_password,
        database=config.db_name
    )
    return pool


async def main(server_address: str):
    """Configuring server settings and starting the server"""

    config = Settings()
    pool = await pool_sql(config)
    orm = Orm(pool)
    logger.info("server for messanger start")
    await server_run(server_address, orm)


if __name__ == '__main__':
    asyncio.run(main('localhost:5000'))
