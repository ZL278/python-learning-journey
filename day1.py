import json
import requests
from pathlib import Path


"""
应对错误：
requests.exceptions.RequestException	请求相关异常的基类，可以捕获大多数请求错误，包括超时和 HTTP 错误
ValueError	JSON 内容无法正常解析时可能出现

区别response.json()和json.dump()
response.json()	HTTP 响应中的 JSON → Python 对象	获取 API 数据
json.dump(data, f)	Python 对象 → JSON 文件	保存数据到文件
"""




url = "https://jsonplaceholder.typicode.com/todos/1"
file_path = Path("todo.json")

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("数据保存成功")

except requests.exceptions.JSONDecodeError:
    print("响应内容不是有效的 JSON")

except requests.exceptions.RequestException as e:
    print(f"请求失败：{e}")


