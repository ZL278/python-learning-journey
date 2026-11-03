import json

"""
typing
给函数添加类型注解
def greet(name: str) -> str:(name: str：提示 name 应该是字符串。)
    return f"你好，{name}"(-> str：提示函数预期返回字符串。)
    
重要：类型注解本身通常不会在运行时自动阻止错误类型。

给列表和字典添加类型注解

str | None:
def find_name(student_id: int) -> str | None:

"""


data = json.loads('{"score": 90, "passed": true, "remark": null}')

print(type(data["score"]))
print(type(data["passed"]))
print(type(data["remark"]))

def get_score(score:int) -> str:
    if score >= 60:
        return "及格"
    else:
        return '不及格'

print(get_score(85))

name: list[str] = ["Alice", "Bob", "Charlie"]
score:dict[str,int]={"Alice":85, "Bob":92}

def find_score(scores:dict[str,int],name:str) -> int | None:
    if name in scores:
        return scores[name]
    return None

for keys in score:
    sco=find_score(score,keys)
    if sco is not None:
        print(f"{keys}:{sco}")


