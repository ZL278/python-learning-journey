import pymysql
from app.db_test2 import db_config

connection = None
try:
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE transaction_practice_accounts
            SET balance = balance - %s
            WHERE user_id = %s
            """,
            (100, 1),
        )
        print("第一条 SQL 已执行：A 账户扣款 100 元")
        cursor.execute(
            """
            UPDATE transaction_practice_accounts
            SET balance = balance + %s
            WHERE user_id = %s
            """,
            (100, 2),
        )
        # connection.commit()
        print("转账成功")

except pymysql.MySQLError:
    if connection is not None:
        connection.rollback()
    print("数据库操作失败，已执行 rollback")
finally:
    if connection is not None:
        connection.close()
