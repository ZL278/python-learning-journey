"""
日志模块 logging
第 1 课：日志基础
日志级别、输出日志、理解日志格式。
这里的 basicConfig(level=logging.DEBUG) 将日志显示门槛设为 DEBUG，因此这五条日志都会输出。
日志级别从低到高：DEBUG < INFO < WARNING < ERROR < CRITICAL

第 2 课：把日志写入文件
logging.FileHandler(log_file, encoding="utf-8")：将日志写入指定文件。

format：自定义日志格式，其中 %(asctime)s 是时间，%(levelname)s 是级别，%(message)s 是日志内容。
handlers：指定日志输出到哪里 streamHandler	输出到流（默认终端） FileHandler	输出到文件
logging.basicConfig() 通常只在根日志记录器尚未配置处理器时生效。

第 3 课：记录异常信息
logging.exception("读取学生成绩文件失败")在
except 代码块中调用，会记录日志消息和当前异常的 traceback
"""

import logging
from pathlib import Path

log_dir=Path.cwd()/"data"/"logs"
log_dir.mkdir(parents=True,exist_ok=True)

log_file=log_dir / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file,encoding="utf-8")
    ]
)


logging.info("正常运行")
logging.warning("警示")
logging.error("错误")
# logging.critical("严重故障")

try:
    with open("missing.txt","r",encoding="utf-8") as f:
        content=f.read()
except OSError:
    logging.exception("文件读取失败")
