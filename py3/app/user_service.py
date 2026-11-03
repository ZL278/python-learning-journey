from app.db import get_db_transaction
from app.crud import get_users_by_cursor
from app.crud import (
    create_user_record,
    get_user_record,
    update_user_record,
    delete_user_record,
    get_users_records
)


def get_users(page: int, page_size: int):
    items, total = get_users_records(page, page_size)
    total_pages = (total + page_size - 1) // page_size
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

def get_users_cursor(cursor_id: int, page_size: int):
    items = get_users_by_cursor(cursor_id, page_size)
    has_more = len(items) > page_size
    items = items[:page_size]
    next_cursor = items[-1]["id"] if items else None

    return {
        "items": items,
        "next_cursor": next_cursor,
        "page_size": page_size,
        "has_more": has_more
    }

def create_user(name: str):
    with get_db_transaction() as connection:
        new_user_id = create_user_record(connection, name)

        return {
            "message": f"User {name} created successfully",
            "name": name,
            "id": new_user_id
        }

def update_user(user_id: int, name: str):
    with get_db_transaction() as connection:
        user = get_user_record(connection, user_id)

        if not user:
            raise ValueError("User not found")

        update_user_record(connection, user_id, name)

        return {
            "message": f"User {name} updated successfully",
            "name": name,
            "id": user_id
        }

def delete_user(user_id: int):
    with get_db_transaction() as connection:
        user = get_user_record(connection, user_id)

        if not user:
            raise ValueError("User not found")

        delete_user_record(connection, user_id)

        return {
            "message": f"User {user_id} deleted successfully"
        }