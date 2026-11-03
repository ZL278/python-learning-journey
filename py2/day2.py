# import pathlib
# from datetime import datetime
"""
datatime获取时间
start = datetime.now()
now.strftime("%Y年%m月%d日 %H时%M分")
"""

# start = datetime.now()
# end = datetime.now()
# duration = (end - start).total_seconds()
# print(duration)
# print(now)
# print(now.strftime("%Y/%m/%d"))
# print(now.strftime("%Y年%m月%d日 %H时%M分"))

"""
os模块
获取当前工作目录 os.getcwd()
读取环境变量 os.getenv("MY_NAME")
"""

# import os
# currentdir = os.getcwd()
# print(f"我的当前工作目录是:{currentdir}")
# value = os.getenv("MY_NAME","未知用户")
# print(value)


"""
Path。你可以把它理解为一个专门表示路径的对象，
它不仅记录文件在哪里，还能帮你创建目录、检查文件是否存在、读取文件等。

from pathlib import Path

data_dir = Path("data")
file_path = data_dir / "todo.json"

print(file_path)
在 Path 对象中，/ 可以用来组合路径
 

4个重要方法
1. exists()：路径是否存在 print(path.exists())
2. is_file()：是不是文件 print(path.is_file())
3. is_dir()：是不是文件夹 print(path.is_dir())
4.data_dir.mkdir(parents=True, exist_ok=True)
创建所需目录；如果上级目录不存在，一并创建；如果目标目录已经存在，也继续运行。

操作方式：
Path.cwd()：获取当前工作目录。
current_dir / "students.json"：拼接路径。不会自动创建 data 目录或 students.json 文件。
.name：获取文件名。
.suffix：获取扩展名。
"""

# from pathlib import Path
# file_path = Path.cwd() / "data/logs"
# file_path.mkdir(parents=True, exist_ok=True)
# print(file_path.exists())
# print(file_path.is_dir())

"""
把今天学的 datetime、os 和 pathlib 组合起来，模拟一个日志目录初始化程序。
"""

from pathlib import Path
from datetime import datetime
cur_time = datetime.now()
time_str = cur_time.strftime("%Y-%m-%d %H:%M:%S")
import os
file_path = Path.cwd() / "data/logs"
file_path.mkdir(parents=True, exist_ok=True)
time_file  = file_path / "app.log"

with time_file.open("a",encoding="utf-8") as f:
    f.write(f"[{time_str}]程序启动\n")
print(f"日志已写入：{time_file}")

