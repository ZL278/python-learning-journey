"""让 Python 真正连接 MySQL"""
"""
Python 通过什么工具连接 MySQL？
Python 如何安全地执行 SQL 并读取结果？
数据库连接信息应该放在哪里，连接失败时怎么排查？
"""

"""
第一步：确认 Python 的 MySQL 驱动
python -m pip install pymysql
2. 尝试登录数据库
mysql -u root -p
输入 mysql -u root -p 失败，
是因为 PowerShell 没有找到这个程序。现在我们直接告诉 PowerShell 程序的完整位置

查找文件：
Get-CimInstance Win32_Service -Filter "Name='MySQL95'" | Select-Object Name, State, PathName
& "C:\Program Files\MySQL\MySQL Server 9.5\bin\mysql.exe" -u root -p:
Python 会把反斜杠 \ 当作转义符的一部分，因此 \P 会触发警告。而且整条命令并不是合法的 Python 语句。

查看端口：
show variables like 'port';

在 PyCharm Terminal 中设置当前终端的密码变量
$env:MYSQL_PASSWORD = Read-Host "请输入 MySQL root 密码"
$env: 是 PowerShell 中访问环境变量的固定前缀
Python 代码里正是用 os.environ["MYSQL_PASSWORD"] 来读取它
Read-Host：这是 PowerShell 的一个内置命令，意思是“读取主机的输入”。
"请输入 MySQL root 密码"：这是传给 Read-Host 的提示语。

"""



"""
day2:让 Python 安全地操作 MySQL
确认一个用于练习的数据库和用户表。
用 Python 查询用户数据。
用 Python 插入用户数据。
学习参数化查询，避免 SQL 注入。
根据实际情况练习修改或删除数据。

DESCRIBE hero;描述、查看结构。在 SQL 中，它通常可以简写为 DESC。
CREATE TABLE practice_users (
    id INT PRIMARY KEY AUTO_INCREMENT,    AUTO_INCREMENT (自动递增)
    name VARCHAR(50) NOT NULL
);


第三步：用 Python 查询用户表
import pymysql
import os

# 假设 connection 已经连接好了（为了演示，这里写一下连接过程）
connection = pymysql.connect(
    host='localhost',
    user='root',
    password=os.environ.get("MYSQL_PASSWORD"),
    database='your_db_name'
)

try:
    # 1. 使用 with 开启游标，结束时会自动 close
    with connection.cursor() as cursor:
        # 2. 准备 INSERT SQL（强烈建议使用 %s 占位符，防止 SQL 注入）
        sql = "INSERT INTO practice_users (name) VALUES (%s)"
        
        # 3. 需要插入的数据（注意这里是个元组，即使只有一个参数也要加逗号）
        参数化传参 (%s)
千万不要 用 f-string 或 + 直接拼接 SQL（如 f"INSERT ... VALUES ('{name}')"），
这会导致严重的安全漏洞（SQL 注入攻击）。cursor.execute(sql, data) 会自动帮你处理转义。
        data = ("张三",) 
        
        # 4. 执行 SQL
        cursor.execute(sql, data)
        
        # 5. 提交事务（如果是增删改，必须 commit 才会真正写入数据库）
        connection.commit()
        print("插入成功！")

except Exception as e:
    # 如果发生错误，回滚事务（撤销之前的操作，保证数据一致性）
    connection.rollback()
    print(f"发生错误，已回滚：{e}")

finally:
    # 6. 无论成功还是失败，最终都会关闭连接
    connection.close()
    print("数据库连接已关闭。")
"""


"""
事务是什么
事务就是一组不可分割的数据库操作，要么全部成功执行，要么全部失败撤销，绝不允许出现“做了一半”的情况。
A (Atomicity) 原子性
C (Consistency) 一致性:数据库的完整性不能被破坏
I (Isolation) 隔离性
D (Durability) 持久性
"""


"""
查询：
        sql = "SELECT * FROM practice_users;"
        result=cursor.execute(sql)
        print(result)
cursor.execute(sql) 的返回值是受影响的行数

sql = "SELECT * FROM practice_users;"
cursor.execute(sql)
# 1. 获取所有查询结果
result = cursor.fetchall() 
# 2. 打印出来看看
print(result) 

fetch 的三种用法：
fetchall()：获取全部数据（最常用）返回一个元组的元组
fetchone()：获取一条数据 每次调用只拿一行数据
fetchmany(size)：获取指定数量的数据

进阶技巧：让结果变成字典
创建游标时指定 pymysql.cursors.DictCursor，数据就会变成字典
connection = pymysql.connect(
    .......
    cursorclass=pymysql.cursors.DictCursor  # 注意这里！
)
"""

"""
rowcount 是 Python 数据库游标（Cursor）对象的一个属性。
用大白话解释：它代表刚刚执行的那条 SQL 语句，到底影响（或查到了）多少行数据。
刚刚的 UPDATE 操作是否真的改动了数据：
写成 if cursor.rowcount != 0:。
"""