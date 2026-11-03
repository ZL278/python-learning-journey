"""
第四周 Day 4：数据库连接管理与事务
"""

"""
数据库事务实战——验证第二条 SQL 失败时，第一条 SQL 能不能一起回滚。
SQL 执行成功，不代表事务已经提交；
只要事务还没提交，发生数据库异常后就可以通过 rollback() 撤销本事务中的修改。
"""

"""
数据库连接管理——从每次手动连接，走向可靠的连接复用。

把数据库连接管理封装起来
解决的是重复代码与资源释放问题。
import os
from contextlib import contextmanager
import pymysql
db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ["MYSQL_PASSWORD"],
    "port": 3306,
    "database": "heima",
    "autocommit": False,
}
@contextmanager
def get_db_connection():
    connection = pymysql.connect(**db_config)

    try:
        yield connection
    finally:
        connection.close()
        
pymysql.connect(**db_config)：创建数据库连接
yield connection：把连接交给调用者，让接口在连接内部执行 SQL。
@contextmanager 让这个函数可以用 with 语句管理资源
contextlib.contextmanager 把一个普通生成器函数变成了一个上下文管理器，可以用 with 语句使用。
核心目的是：自动管理数据库连接的创建和关闭
"""

"""
with get_db_connection() as conn:
进入一个上下文，把 get_db_connection() 交给你的资源（这里是数据库连接）绑定到变量 conn，用完自动做清理
"""


"""
连接池
连接池不是让所有请求同时使用同一个连接，而是管理多个连接，按需分配和回收。
使用 DBUtils 建立连接池
python -m pip install DBUtils
# 创建连接池
pool = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=5,
    blocking=True,
    **db_config
)

mincached ≤ maxcached ≤ maxconnections，这是合理配置
mincached=2：启动时已有 2 条，前两个请求秒连
并发涨到 10 条时用满 maxconnections，第 11 个请求在 blocking=True 下排队
请求回落后，空闲连接最多留 5 条（maxcached），多出来的被回收
"""

"""
把连接池接入 FastAPI，让真实接口复用连接。
"""

"""
Python 的 logging 使用统一的日志管理机制，两个 logger 可以使用同一套配置。
"""

"""
数据库错误应该由谁处理？db.py 处理，还是 FastAPI 接口处理？
谁负责创建和管理资源，谁就负责释放资源；谁掌握业务含义，谁就负责业务判断。
db.py：数据库基础设施层
main.py：业务接口层
客户端 / Swagger
"""

"""
return {...}
虽然写在 with 内部，但 Python 会先退出 with，执行连接管理器中的 connection.commit()，然后才真正返回响应

后端项目很重要的设计思想：
业务层负责业务，基础设施层负责基础设施，异常在不同层之间传递并被恰当地处理。
"""