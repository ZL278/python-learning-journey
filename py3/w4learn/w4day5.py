"""
分层思想
db_test2.py 负责 API，但 SQL 语句仍然全部写在 API 路由函数里。
"""

"""
分层思想
API 路由层（FastAPI）接收 HTTP 请求、处理响应和状态码
业务层（Service）处理业务规则、组织业务流程
数据访问层（CRUD / Repository）编写 SQL、执行数据库读写
db.py 连接池、连接管理、事务管理
"""

"""
循环导入：
db_test2.py 导入 crud.py
  - crud.py 又导入 db_test2.py 里的 Person
  Person 是 Pydantic 模型，却被两个文件互相依赖。最干净的解决办法是把 Person
  抽到一个独立的 schemas.py，让两边都从那里导入。
"""

"""
共享同一个事务
假设用户购买一件商品，后端需要执行两条 SQL,多个数据库操作共享同一个数据库连接、同一个事务边界。
文件	负责什么
db.py	提供事务上下文，统一提交或回滚

crud.py	执行具体 SQL，不提交、不回滚,
应该关心数据库执行结果，而不是接口最终要向用户展示什么消息。
rowcount 表示受 SQL 影响的行数。
- 1：影响了一行。
- 0：没有行受到影响。
UPDATE 将用户姓名修改成原本相同的值时，MySQL 对受影响行数的报告可能是 0，
所以不能简单地把 rowcount == 0 一律理解成用户不存在。我们会在 Service 层结合事务内的查询处理。

user_service.py	组织多个数据库操作，决定它们是否属于同一个事务

db_test2.py	接收 HTTP 请求、返回 HTTP 响应

def create_user_record(connection, name):
connection 由外部传入，不在这个函数里重新获取连接。
"""

"""
分页查询
现在你的 GET 接口：
SELECT id, name FROM practice_users
真实项目通常采用分页：
GET /users?page=1&page_size=10
"""

"""
数据库集成与分页
│
├── 数据库连接
│   ├── PyMySQL
│   └── DBUtils 连接池
│
├── 事务管理
│   ├── commit
│   └── rollback
│
├── 分层架构
│   ├── API：HTTP 接口
│   ├── Service：业务逻辑
│   └── CRUD：SQL 操作
│
└── 分页查询
    ├── OFFSET 分页
    │   ├── LIMIT
    │   └── OFFSET
    │
    └── 游标分页
        ├── WHERE id > cursor_id
        ├── LIMIT page_size + 1
        ├── has_more
        └── next_cursor
"""

"""
total_pages = (total + page_size - 1) // page_size:
在 Python 里，/ 是浮点数除法，会得到小数；// 是向下取整（Floor Division），会砍掉小数部分
如果你想让结果“只要有一点小数就进 1”，最简单的办法就是给被除数加上一个刚好差一点点就能进位的值。
"""

"""
两种分页方式对比
OFFSET 分页
LIMIT 10 OFFSET 100000从前面开始，跳过大量记录，再取数据。
GET /users?page=2&page_size=10
{
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }
    
    
游标分页
WHERE id > 100000 LIMIT 10根据上次的位置继续向后查询。

has_more 有一个小缺陷：如果最后一批数据刚好有 10 条，但后面已经没有记录，它仍然会返回 true
每次多查询一条记录。
cursor.execute(sql, (cursor_id, page_size+1))
has_more = len(items) > page_size
    items = items[:page_size]
    next_cursor = items[-1]["id"] if items else None
    
    
GET /users?cursor=10&page_size=10
{
    "items": [
        {"id": 11, "name": "张三"},
        {"id": 12, "name": "李四"}
    ],
    "next_cursor": 20,
    "page_size": 10
}
"""

"""
Day 7：第四周项目验收。
检查是否具备工程交付能力
1. 数据库设计与持久化
MySQL 表结构、主键、自增 ID、数据持久化、参数化 SQL。

2. 数据库连接管理
DBUtils 连接池、连接归还、异常情况下的资源释放。

3. 事务与数据一致性
commit、rollback、事务边界、业务异常与数据库异常的区分。

4. 分层架构
API、Service、CRUD 的职责是否清晰，依赖方向是否合理。

5. 分页设计
OFFSET 分页、游标分页、参数限制、next_cursor、has_more。

6. 工程规范与安全
环境变量、.gitignore、日志、异常响应、项目结构、README。
"""

