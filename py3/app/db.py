import os
from contextlib import contextmanager

import pymysql
from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv

load_dotenv()

import logging

logger = logging.getLogger(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("MYSQL_PASSWORD"),
    "port": 3306,
    "database": "heima",
    "autocommit": False,
    "cursorclass": pymysql.cursors.DictCursor
}

pool=PooledDB(
    creator = pymysql,
    maxconnections=10,
    mincached =2,
    maxcached=5,
    blocking=True,
    **db_config
)
logger.info("Database connection pool initialized")

@contextmanager
def get_db_connection():
    connection = pool.connection()

    try:
        yield connection
    finally:
        connection.close()

@contextmanager
def get_db_transaction():
    connection = pool.connection()

    try:
        yield connection
        connection.commit()

    except pymysql.MySQLError:
        logger.exception("Database operation failed")
        connection.rollback()
        raise
    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()