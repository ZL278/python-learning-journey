# Python 用户管理后端项目

一个基于 **FastAPI + MySQL** 开发的用户管理后端项目，主要用于实践 Python 后端开发中的数据库集成、分层架构、连接池、事务管理和分页查询。

## 1. 项目介绍

本项目实现了一个基础的用户管理 RESTful API，支持用户的创建、查询、修改和删除。

在基础 CRUD 功能之外，项目还实现了：

- 使用 PyMySQL 连接 MySQL 数据库
- 使用 DBUtils 管理数据库连接池
- 使用事务管理保证写操作的数据一致性
- 采用分层架构，将 API、业务逻辑和 SQL 操作分离
- 支持 OFFSET 分页和 Cursor 游标分页
- 使用 Pydantic 进行请求参数校验
- 使用 Python logging 记录异常信息
- 使用环境变量管理数据库配置

## 2. 技术栈

| 技术 | 用途 |
|---|---|
| Python | 后端开发语言 |
| FastAPI | Web API 框架 |
| MySQL | 关系型数据库 |
| PyMySQL | Python MySQL 驱动 |
| DBUtils | 数据库连接池 |
| Pydantic | 请求数据校验 |
| python-dotenv | 加载环境变量 |
| Uvicorn | ASGI 服务运行器 |

## 3. 项目结构

```text
py3/
├── db_test2.py       # FastAPI 应用入口及 API 路由
├── schemas.py        # Pydantic 数据模型
├── user_service.py   # 业务逻辑层
├── crud.py           # 数据库 SQL 操作层
├── db.py             # 数据库配置、连接池及事务管理
├── .env              # 数据库环境变量（不上传 GitHub）
├── .gitignore        # Git 忽略配置
└── README.md         # 项目说明文档
```

### 分层职责

**API 层（db_test2.py）**

接收 HTTP 请求、调用 Service 层、处理异常并返回响应。

**Schema 层（schemas.py）**

使用 Pydantic 定义请求数据结构和字段校验规则。

**Service 层（user_service.py）**

组织业务流程，调用 CRUD 层，并通过事务上下文管理写操作。

**CRUD 层（crud.py）**

负责具体 SQL 执行，包括查询、插入、修改、删除和分页查询。

**数据库层（db.py）**

负责数据库配置、连接池初始化、连接获取和事务提交、回滚。

## 4. 数据库配置

项目使用 MySQL 数据库。

首先创建数据库：

```sql
CREATE DATABASE heima;
```

选择数据库：

```sql
USE heima;
```

创建用户表：

```sql
CREATE TABLE practice_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);
```

在项目根目录创建 `.env` 文件：

```env
MYSQL_PASSWORD=你的MySQL密码
```

数据库连接配置通过环境变量读取，不应将真实数据库密码直接写入代码或提交到 GitHub。

## 5. 安装与运行

### 5.1 创建虚拟环境

```powershell
python -m venv .venv
```

激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5.2 安装依赖

如果项目已经准备好 `requirements.txt`：

```powershell
python -m pip install -r requirements.txt
```

如果尚未生成依赖文件，可以在当前虚拟环境中安装项目所需依赖：

```powershell
python -m pip install fastapi uvicorn pymysql DBUtils python-dotenv
```

### 5.3 启动项目

在项目根目录执行：

```powershell
uvicorn db_test2:app --reload
```

启动后访问：

- API 文档：`http://127.0.0.1:8000/docs`
- OpenAPI JSON：`http://127.0.0.1:8000/openapi.json`

## 6. API 接口

基础接口统一使用 `/users` 路径。

| 请求方法 | 接口路径 | 功能 |
|---|---|---|
| POST | `/users` | 创建用户 |
| GET | `/users` | OFFSET 分页查询用户 |
| GET | `/users/cursor` | Cursor 游标分页查询 |
| PUT | `/users/{user_id}` | 修改用户 |
| DELETE | `/users/{user_id}` | 删除用户 |

### 6.1 创建用户

`POST /users`

请求示例：

```json
{
    "name": "Alice"
}
```

### 6.2 OFFSET 分页查询

`GET /users?page=1&page_size=10`

使用页码和每页数量进行分页查询，同时返回总记录数和总页数。

### 6.3 Cursor 游标分页

`GET /users/cursor?cursor_id=0&page_size=10`

通过上一批数据的最后一个用户 ID 获取下一批数据，并返回：

- `items`：当前页数据
- `next_cursor`：下一次查询使用的游标
- `page_size`：每页数量
- `has_more`：是否还有更多数据

### 6.4 修改用户

`PUT /users/{user_id}`

请求示例：

```json
{
    "name": "Bob"
}
```

### 6.5 删除用户

`DELETE /users/{user_id}`

根据用户 ID 删除对应记录。

## 7. 项目中的工程实践

### 数据库连接池

使用 DBUtils 的 `PooledDB` 管理数据库连接，减少频繁创建和销毁连接的开销。

### 事务管理

写操作通过事务上下文管理：

- 操作成功：提交事务 `commit()`
- 操作失败：回滚事务 `rollback()`

确保同一事务中的数据库操作保持一致性。

### 参数化 SQL

数据库操作使用 `%s` 参数占位符传递参数，避免直接拼接用户输入，降低 SQL 注入风险。

### 分层架构

将 API 路由、业务逻辑、SQL 操作和数据库连接管理分开，降低模块之间的耦合，提高代码可维护性。

### 分页查询

实现两种分页方式：

- OFFSET 分页：适用于需要按页码跳转的查询场景。
- Cursor 分页：适用于连续加载数据的场景，避免深分页带来的部分性能问题。

## 8. 后续改进方向

- 将项目入口整理为标准 Python 包结构
- 增加自动化测试
- 完善统一异常处理
- 增加用户认证与权限管理
- 增加 Docker 部署支持
- 完善 API 日志与监控

## 9. 项目目的

通过本项目，实践 Python 后端开发的核心流程：

**HTTP 请求 → FastAPI → Schema 校验 → Service 业务处理 → CRUD SQL 操作 → MySQL 数据库**

项目是个人 Python 后端学习过程中的阶段性实践作品，后续将继续扩展为更加完整的后端应用。