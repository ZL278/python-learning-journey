"""
第 1 课：创建虚拟环境
python -m venv .venv：命令会在当前目录下创建环境，但不会自动激活
.venv\Scripts\activate.bat 激活虚拟环境
确认 Python 解释器的实际路径
python -c "import sys; print(sys.executable)"

生成依赖清单
python -m pip freeze > requirements.txt
pip：包管理工具:负责安装、卸载、查看和管理 Python 第三方库。
> 是 shell 的输出重定向符号,文件不存在，就创建；如果已存在，会清空覆盖。
追加而不是覆盖，用 >>

复现环境:
别人python -m pip install -r requirements.txt 装一样的包

5 个命令
python -m pip list	查看当前环境已安装的包
python -m pip show requests	查看某个包的版本、安装位置等信息
python -m pip install requests	安装包
python -m pip uninstall requests	卸载包，会要求确认
python -m pip install -r requirements.txt	按清单安装依赖

查看版本
python -c "import requests; print(requests.__version__)"
-c 是 command 把后面引号里的字符串当作代码直接执行，而不是去运行一个 .py 文件
引号里可以写多条语句，用分号 ; 隔开
"""