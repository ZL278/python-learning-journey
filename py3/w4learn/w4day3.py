"""
try...except...finally 结构：
这是数据库操作的标准框架。
如果数据库断开或 SQL 报错，进入 except 并 rollback() 保证数据一致性；最后 finally 确保连接被关闭。
"""

"""
DB_CONFIG 字典：
把连接参数抽离出来，方便修改和复用
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("MYSQL_PASSWORD"), 
    "database": "your_database_name",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor 
}

connection = pymysql.connect(**DB_CONFIG)
** 叫做“解包”操作符,加了 ** 之后，Python 会自动把字典里的键值对拆开
"""


"""
创建一个 .env 文件,MYSQL_PASSWORD=你的真实密码
安装库：pip install python-dotenv
.env 文件不要提交到 Git，应该在 .gitignore 里忽略它
from dotenv import load_dotenv
import os
load_dotenv() # 这行代码会自动把 .env 文件里的变量加载到环境中

mysql -u root -p：是你本人用客户端去连数据库，必须你手动敲密码。（.env 管不着）
python db_test.py：是你的 Python 代码去连数据库，代码可以通过 .env 自动拿到密码。（不用你敲）
连同一个库：密码必须一样
"""


"""
函数返回值：
@app.get("/users")
def get_users():
单条数据：返回一个字典 {...}。
多条数据：返回一个列表 [{...}, {...}]。
规范化：使用 DictCursor 能让你从数据库取出的数据天然就是字典，
"""

"""
new_user_id = cursor.lastrowid
获取最近一次插入操作生成的自增 ID。
"""

"""
后端常用的错误分类思路:
收到修改用户请求
Pydantic 校验请求数据:失败 → 422
尝试连接数据库并查询用户:连接失败 → 500 / 503
检查用户是否存在:不存在 → 404
执行 UPDATE 并提交事务:SQL 或事务失败 → 500
"""

"""
RequestValidationError（框架自动处理）：
HTTPException（你需要主动处理）
raise 语句的作用就是立即中断当前函数的正常执行流程，并抛出一个异常
当你在 try 块里主动 raise HTTPException(404) 时，这个异常不会被 except pymysql.MySQLError 抓住，
它会继续往上抛，最终被 FastAPI 的异常处理器接管，正确返回 404 响应给客户端。
"""


"""
看服务端日志，判断到底是数据库连接失败，还是 SQL 执行失败。
一、先理解两类故障的区别
情况 A：数据库连接失败
发生在 pymysql.connect(**db_config) 阶段，程序还没开始执行 SQL。

情况 B：SQL 执行失败
连接已经成功，但在 cursor.execute(...) 等数据库操作阶段出错。

连接失败不一定代表 MySQL 服务没启动；
SQL 执行失败也不一定是 SQL 语法错误。我们要结合异常类型、错误代码和发生位置判断。

二、给你的 FastAPI 项目加上服务端日志
第 1 步：在文件开头配置日志
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)
这是对根日志记录器（Root Logger）进行全局的基础配置
“获取一个日志记录器，并且用当前文件的名字来给它命名。”
__name__是 Python 中的一个内置变量（魔法变量）。“当前这个文件所在的位置”作为日志的名字打出来
"""

"""
__name__这是 Python 官方约定俗成的一种命名规范
Python 官方决定给所有“系统内置的、特殊的、不想让用户随便覆盖的”变量和函数，都加上双下划线前缀和后缀
单下划线 _name：通常表示“内部使用”（比如类的私有变量）
双下划线 __name__Python 语言级别的魔法方法（Magic Methods）或特殊属性。
"""

"""
脚本 = 能够被直接启动并执行一段完整逻辑的代码文件
在 Python 语境下，几乎一切都是“脚本”
在 Python 里，每一个 .py 文件都可以被称为一个脚本
脚本（Script）：通常指那些直接运行就能完成某个具体任务的文件,通常是程序的入口
模块（Module）：通常指那些不直接运行，而是被其他代码 import 进去使用的文件
"""
