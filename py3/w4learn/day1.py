"""
理解客户端、服务器和 HTTP 的关系
[ ] 理解请求（Request）与响应（Response）
[ ] 认识 GET、POST、PUT、DELETE
[ ] 分清 Path、Query、Header、Body
[ ] 认识常见状态码与 JSON
[ ] 能够读懂一个简单的 HTTP 请求和响应
"""

"""
requests
客户端 Client发出请求的一方，例如浏览器、Python 程序。
HTTP 请求与响应通过网络通信
服务器 Server 接收请求、执行逻辑并返回结果，例如网站的后端服务。

requests：让你的程序作为客户端，向其他服务发送请求
FastAPI：让你的 Python 程序作为服务器，接收其他客户端的请求。
"""

"""
HTTP 请求与响应是什么
请求 Request
GET /users/12 HTTP/1.1
Host: localhost:8000
Accept: application/json
请求方法：GET,路径：/users/12,请求头 Header

响应 Response
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 12,
  "name": "Alice"
}
状态码：200,响应体 Body包含实际返回的数据，这里是一个 JSON 对象。
HTTP 请求不一定有 Body。
"""

"""
四种常见的 HTTP 请求方法
方法	常见用途	用户管理 API 示例
GET	查询资源	GET /users 查询所有用户
POST	创建资源或提交处理	POST /users 新增用户
PUT	整体更新资源（常见约定）	PUT /users/12 更新用户 12
DELETE	删除资源	DELETE /users/12 删除用户 12
"""


"""
Path、Query、Header、Body 有什么区别
GET /users/12?include_email=true
Accept: application/json

Path · 路径参数
/users/12 中的 12,表示要查询的具体用户，通常用于标识资源。

Query · 查询参数,?include_email=true
表示附加查询条件或选项，通常位于路径后面，以 ? 开始；多个参数可以用 & 连接。

Header · 请求头
Accept: application/json,传递元信息，这里表示客户端希望接收 JSON 格式的响应。
Header 是在 “数据解包” -> “全局拦截” -> “参数提取” 这三个连续环节中发挥作用

Body · 请求体
创建用户时提交的数据，专门用来接收用户发来的数据。
"""


"""
五、常见 HTTP 状态码
状态码	含义	例子
200 OK	请求成功	查询用户成功
201 Created	资源创建成功	成功新增用户
403 Forbidden	不允许执行该操作	已识别身份，但没有权限
404 Not Found	资源或路径不存在	查询不存在的用户
422 Unprocessable Content	请求内容未通过相应校验	FastAPI 常见的请求数据校验失败

response.raise_for_status()
它会在响应状态码表示 HTTP 错误（通常为 4xx 或 5xx）时抛出异常
"""