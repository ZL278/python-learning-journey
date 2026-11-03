from http.client import HTTPException
from pydantic import BaseModel,Field
from fastapi import FastAPI,Header,Query,HTTPException

app = FastAPI()
class UserCreate(BaseModel):
    name: str=Field(min_length=1,max_length=20)
user_db=[]

@app.get("/")
def home():
    return {"message": "Hello Python Intern!"}
@app.get("/about")
def about():
    return {"goal":"FASTAPI","week":"第三周"}

@app.get("/search")
def search_users(limit:int =10):
    return {
        "limit":limit,
        "message":"查询用户列表"
    }


@app.post("/users")
def create_user(user:UserCreate):
    new_user ={
        "id":len(user_db)+1,
        "name":user.name,
    }
    user_db.append(new_user)
    return{
        "message": "用户创建成功",
        "data": new_user
    }
@app.get("/users")
# default=10：默认值，ge=1,le=10：大于等于 1、小于等于 10
def get_users(limit:int =Query(default=10,ge=1,le=10)):
    return {
        "count":len(user_db[:limit]),
        "data":user_db[:limit]
    }

@app.get("/client-info")
def client_info(user_agent:str | None = Header(None)):
    return {
        "user_agent": user_agent
    }

@app.get("/users/{user_id}")
def get_user(user_id:int):
    for user in user_db:
        if user["id"] == user_id:
            return user

    # from fastapi import HTTPException 注意要导入
    raise HTTPException(
        status_code=404,
        detail="用户不存在"
    )

@app.put("/users/{user_id}")
# 真实业务中，用户 ID 不一定连续，不能依赖 ID 和列表位置的对应关系。
def update_user(user_id:int,user:dict):
    for item in user_db:
        if item["id"] == user_id:
            item.update(user)
            return item
    raise HTTPException(
        status_code=404,
        detail="用户不存在"
    )

@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    for item in user_db:
        if item["id"] == user_id:
            user_db.remove(item)
            return {
                "message":f"成功删除用户{user_id}"
            }
    raise HTTPException(
        status_code=404,
        detail="用户不存在"
    )


"""
Day 6：Pydantic 数据校验与 HTTP 异常处理。
1. 为什么需要 Pydantic？
防止用户提交缺少姓名、类型错误或不合理的数据。

2. 使用模型定义请求数据
从随意接收 dict，升级到有明确字段和规则的数据模型。

3. 规范处理错误
理解 200、201、404、422、500 的区别，以及什么时候应该使用它们。
"""

"""
第二步：创建第一个 Pydantic 模型
from pydantic import BaseModel
class UserCreate(BaseModel):
    name: str  创建用户时，必须提供一个字符串类型的 name。
接入：def create_user(user: UserCreate):

如何规定字段的具体校验规则。
修改你的模型
from pydantic import BaseModel, Field
class UserCreate(BaseModel):
    name: str=Field(min_length=1,max_length=20)
    Field(...)	为这个字段增加约束
min_length=1	至少包含 1 个字符
max_length=50	最多包含 50 个字
设置别名 (Alias) Field(..., alias="userName") 驼峰命名 userName
"""

"""
Day6 HTTP 异常处理——
让 API 遇到问题时，返回明确、合理的错误信息，而不是莫名其妙地报错
200	请求成功	成功查到用户
404	请求的资源不存在	查询 ID 为 999 的用户，但该用户不存在
422	请求数据未通过校验	创建用户时没有提供必填的 name
500	服务器内部发生未妥善处理的错误	代码出现未处理的异常
"""