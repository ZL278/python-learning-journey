from fastapi import FastAPI,HTTPException, Query

import pymysql
from user_service import (
    create_user,
    update_user,
    delete_user,
    get_users,
    get_users_cursor
)
from schemas import Person

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
app=FastAPI()


@app.post("/users")
def create_user_api(user: Person):
    try:
        return create_user(user.name)
    except pymysql.MySQLError:
        logger.exception("Failed to create user")
        raise HTTPException(status_code=500, detail="Database operation failed")


@app.get("/users")
def get_users_api(
        page: int = Query(default=1,ge=1),
        page_size: int = Query(default=10,ge=1,le=100)

):
    try:
        return get_users(page, page_size)
    except pymysql.MySQLError:
        logger.exception("Failed to get users")
        raise HTTPException(status_code=500, detail="Database operation failed")


@app.get("/users/cursor")
def get_users_cursor_api(
    cursor_id: int = Query(default=0, ge=0),
    page_size: int = Query(default=10, ge=1, le=100)
):
    try:
        return get_users_cursor(cursor_id, page_size)

    except pymysql.MySQLError:
        logger.exception("Failed to get users by cursor")
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )



@app.put("/users/{user_id}")
def update_user_api(user_id: int, user: Person):
    try:
        return update_user(user_id, user.name)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    except pymysql.MySQLError:
        logger.exception("Failed to update user")
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )



@app.delete("/users/{user_id}")
def delete_user_api(user_id: int):
    try:
        return delete_user(user_id)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    except pymysql.MySQLError:
        logger.exception("Failed to delete user")
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )
