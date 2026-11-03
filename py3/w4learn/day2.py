from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message": "Hello Python Intern!"}
@app.get("/about")
def about():
    return {"goal":"FASTAPI","week":"第三周"}


# FastAPI
# 基于 Python 类型提示构建 API 的高性能 Web 框架
"""
学习目标
目标 1：安装 FastAPI 和 Uvicorn
目标 2：编写第一个接口
目标 3：独立启动并测试
"""

"""
理解三个角色
浏览器
Uvicorn（接收 HTTP 请求）
FastAPI（匹配接口、执行函数）
返回 JSON 响应
"""

"""
第一步：安装 FastAPI 和 Uvicorn
python -m pip install fastapi "uvicorn[standard]"
FastAPI 本身只是一个“应用框架”，它不能直接对外提供网络服务
 Uvicorn（服务器）就是监听端口、接收 HTTP 请求，然后转交给你的 FastAPI 应用去处理。
 相当于：FastAPI 是“厨子”，Uvicorn 是“服务员”。
 [standard]表示安装 Uvicorn 的可选依赖组（Extras）
"""

"""
创建第一个 API
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message": "Hello fastapi"}
    
应用对象 app：承载你定义的 API 接口
装饰器 @app.get("/about")：将 HTTP 方法和 URL 路径关联到函数。
返回值 return {...}：将 Python 数据交给 FastAPI，转换成 HTTP 响应。
"""

"""
启动服务并测试
python -m uvicorn main:app --reload
main：main.py 文件名，不需要写 .py。
app：文件中创建的 FastAPI 应用对象。
--reload：开发时监测代码修改，并在需要时自动重启服务

127.0.0.1	IP 地址	本地回环地址，通常也叫 localhost。意思是“本机”
http://127.0.0.1:8000/docs是 FastAPI 自动生成的 Swagger UI 测试页面
"""