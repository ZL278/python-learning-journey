from pathlib import Path
import json

"""
关键知识点：合法 JSON 不代表解析后一定是字典。 
它也可能是列表、字符串、数字、布尔值或 None。

数据检查可以分为三个层次：
第一层：文件检查
路径存在吗？它是文件吗？
第二层：结构检查
JSON 能解析吗？解析后是字典吗？有 title 吗？
第三层：字段值检查
title 的值是不是字符串？是否为空？
"""

file_path= Path("todo.json")
if file_path.is_file():
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            if "title" in data:
                if isinstance(data["title"], str):
                    if data["title"].strip():
                        print(data["title"])
                    else:
                        print("title 不能为空")
                else:
                    print("title 必须是字符串")
            else:
                print("数据中没有 title 字段")
        else:
            print("JSON 数据不是字典")

    except json.decoder.JSONDecodeError:
        print("JSON格式错误")
else:
    print("文件不存在")
