from http.client import HTTPException

from fastapi import FastAPI,Header,Query,HTTPException
app = FastAPI()
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
def create_user(user:dict):
    user["id"]=len(user_db)+1
    user_db.append(user)
    return{
        "message": "用户创建成功",
        "data": user
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
构建真正的用户管理 API（一）
一、先理解我们正在构建什么
前端页面 / API 客户端(提交用户信息、请求用户列表)
FastAPI 后端(接收请求 → 执行业务逻辑 → 返回 JSON)
内存中的用户列表(暂时模拟数据库，保存本次运行期间创建的用户)

二、第一步：让创建用户真正产生效果
1. 在 main.py 中创建模拟数据库
# 模拟数据库：保存用户数据
users_db = []
"""

"""
重看json和dict的区别：
特性	Python 字典 (dict)	JSON
本质	内存中的数据结构（对象）	文本字符串（String）
键的引号	单双引号都可以	只能用双引号
布尔/空值	True / False / None	true / false / null
作用范围	仅在 Python 代码内部	跨语言、跨网络（前后端、API）
互相转换	json.dumps() 转出 ->	<- json.loads() 转入
记住：字典是“活的”（可变、可操作），JSON 是“死的”（纯文本、只负责传输）。
"""

"""
构建真正的用户管理 API（二）
查询单个用户、修改用户、删除用户
# from fastapi import HTTPException 注意要导入

def update_user(user_id:int,user:dict):
    for item in user_db:
        if item["id"] == user_id:
            # 给变量重新赋值，不等于修改列表里原来的数据。
            # item暂时指向列表中Alice对应的字典。
            # item = user让变量item改为指向请求Body中的新字典。
            # user_db列表本身没有发生变化。
            # item=user
            可以使用item.update(user)：update() 会把 user 字典中的键值更新到原来的 item 字典中。
            因为 item 指向的就是列表里的那个字典，所以列表中的数据也会同步变化。

DELETE /users/{user_id}
user_db.remove(item)
"""



