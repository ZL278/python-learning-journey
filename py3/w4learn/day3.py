from fastapi import FastAPI,Header
app = FastAPI()
@app.get("/")
def home():
    return {"message": "Hello Python Intern!"}
@app.get("/about")
def about():
    return {"goal":"FASTAPI","week":"第三周"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id,
    }
@app.get("/search")
def search_users(limit:int =10):
    return {
        "limit":limit,
        "message":"查询用户列表"
    }
@app.post("/users")
def create_user(user:dict):
    return{
        "received_user": user
    }
@app.get("/client-info")
def client_info(user_agent:str | None = Header(None)):
    return {
        "user_agent": user_agent
    }



# FastAPI 的请求参数：Path、Query、Body 和 Header。

"""
一、先把四种参数弄明白
Path：我要操作哪个资源？
Query：我要怎样筛选或查询？
Body：我要提交什么数据？
Header：这次请求还携带了哪些元信息？
"""

"""
1. Path：从 URL 路径中获取参数
"/users/{user_id}"：花括号表示这是一个动态路径参数
@app.get("/users/{user_id}")
def get_user(user_id: int):
     # 第一步：拿着 user_id 去数据库里查这个人的真实信息
      # 第二步：把数据库查出来的结果返回给用户
    return {
        "user_id": user_id,
        "message": "查询指定用户"
    }
    
2. Query：从问号后面获取查询条件(写在 ? 后面，用 & 连接。)
@app.get("/search")
def search_users(limit: int = 10,keyword: str = ""):
    # 真实场景：拿着 limit 去数据库里限制查询的数量
    # 假设这里去数据库查数据，只取前 limit 条
    users = 数据库.查询(sql="SELECT * FROM users LIMIT ?", limit) 
    
    return {
        "count": limit,
        "data": users,
        "message": f"成功返回了 {limit} 条用户数据"
    }
    
    
3. Header 请求头
数据解包” -> “全局拦截” -> “参数提取
User-Agent	说明客户端使用什么软件发起请求
Authorization	携带身份验证凭证
Content-Type	说明请求体的数据类型，例如 JSON

user_agent：Python 函数中接收请求头的变量。
str | None：表示它可以是字符串，也可以是 None。
Header(...)：告诉 FastAPI，这个参数应该从 HTTP 请求头中读取。
default=None：即使请求中没有对应的请求头，也允许它为空。
"""


"""
重看API：
@app.get("/search") 加上下面的函数，就是一个 API。
API 就是前后端分离的“合同”
Path、Query、Body：是你调用 API 时，往里面塞数据的不同“坑位”。
Header：是你调用 API 时的“身份证”或“通行证”（比如证明你是 VIP，才能查数据）。
422 错误：是你没按 API 的规矩塞数据（比如要数字你塞了字母），API 把你拒绝了。
Swagger UI（/docs 页面）：这就是 FastAPI 自动给你生成的 API 说明书，
"""
