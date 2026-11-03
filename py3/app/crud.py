from db import get_db_connection

def get_users_records(page:int,page_size:int):
    offset = (page-1)*page_size
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            count_sql = "SELECT COUNT(*) AS total FROM practice_users"
            cursor.execute(count_sql)
            total = cursor.fetchone()["total"]
            sql = """
                SELECT id, name
                FROM practice_users
                ORDER BY id
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (page_size, offset))
            items = cursor.fetchall()
            return items, total


def get_users_by_cursor(cursor_id: int, page_size: int):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            sql = """
                SELECT id, name
                FROM practice_users
                WHERE id > %s
                ORDER BY id
                LIMIT %s
            """
            cursor.execute(sql, (cursor_id, page_size+1))
            return cursor.fetchall()


def get_user(user_id: int):
    with get_db_connection() as connection:
        return get_user_record(connection, user_id)


def get_user_record(connection,user_id:int):
    with connection.cursor() as cursor:
        sql = "SELECT id from practice_users WHERE id=%s"
        cursor.execute(sql, (user_id,))
        return cursor.fetchone()


def create_user_record(connection,name:str):
    with connection.cursor() as cursor:
        sql = "INSERT INTO practice_users (name) VALUES (%s)"
        data = (name,)
        cursor.execute(sql, data)
        new_user_id = cursor.lastrowid
        return new_user_id


def update_user_record(connection,user_id: int, name:str):
    with connection.cursor() as cursor:
        sql = "UPDATE practice_users SET name=%s WHERE id=%s"
        data = (name, user_id)
        cursor.execute(sql, data)
        return cursor.rowcount


def delete_user_record(connection,user_id: int):
    with connection.cursor() as cursor:
        sql = "DELETE FROM practice_users WHERE id=%s"
        data = (user_id,)
        cursor.execute(sql, data)
        return cursor.rowcount
