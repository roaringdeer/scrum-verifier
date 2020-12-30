from fastapi import FastAPI
from databases import Database
from app.core.config import DATABASE_URL
import logging, os

logger = logging.getLogger(__name__)

async def get_db():
    # these can be configured in config as well
    db_url = f'''{DATABASE_URL}{os.environ.get('DB_SUFFIX', '')}'''
    return Database(db_url, min_size=2, max_size=10)

async def connect_to_db(app: FastAPI) -> None:
    database = await get_db()
    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warn('--- DB CONNECTION ERROR ---')
        logger.warn(e)
        logger.warn('--- DB CONNECTION ERROR ---')

async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn('--- DB DISCONNECT ERROR ---')
        logger.warn(e)
        logger.warn('--- DB DISCONNECT ERROR ---')
