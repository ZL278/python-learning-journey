#浏览器能打开 GitHub，但 Git 命令却无法连接 GitHub。的解决办法
#GitHub 网络连接故障排查笔记

"""
故障案例
浏览器可以打开 GitHub，但 git fetch / git pull 失败
已定位原因方向
Windows PowerShell
HTTPS 443

环境：Windows、Git、PowerShell、Python 虚拟环境、代理地址 127.0.0.1:7897。
"""

"""
一、先弄懂：到底出了什么问题？
报错	通俗解释	优先检查方向
Connection was reset	连接被中途重置	网络链路、代理、连接稳定性
Connection timed out	等待连接超时	网络是否可达、代理是否生效、防火墙等
Could not resolve host	无法解析域名	DNS、网络配置
Authentication failed	身份验证失败	登录凭据、令牌、权限
CONFLICT	合并冲突	本地和远程代码如何整合

GitHub 网页能打开，不代表 Git 一定能访问 GitHub。浏览器和 Git 可能使用不同的代理设置。
"""

"""
二、我们是怎样一步一步找到问题的？
第 1 步：检查 Git 远程仓库地址
git remote -v
第 2 步：检查 Git 是否配置了代理
git config --show-origin --get-regexp "http\..*proxy"
git config --show-origin --get-regexp "https\..*proxy"
两条命令都没有输出。说明 Git 的配置中没有匹配到这两类代理项,它不代表代理软件没有开启

Git 配置和 Windows 代理设置不是同一回事。

Get-ChildItem Env: | Where-Object { $_.Name -match 'proxy' }
没有输出，说明当前 PowerShell 会话中没有名称包含 proxy 的环境变量
只说明当前环境变量的情况，并不能证明系统所有代理配置都不存在

命令行工具确实优先读环境变量
Git（底层 libcurl）、curl、wget、Python 的 requests 等，默认都会读取 HTTP_PROXY / HTTPS_PROXY 环境变量。
排查代理
git config 里的代理  →  环境变量里的代理  →  Windows 系统代理  →  应用自己的设置


关键：Windows 有「三套」代理配置
这是最容易搞混的地方。Windows 上不同组件读不同的代理设置：

层	谁在用	在哪配置	查看命令
WinINET	IE、Edge、Chrome（部分）、系统「代理设置」	注册表 HKCU\...\Internet Settings	设置界面 / 注册表
WinHTTP	Windows 服务、部分系统程序、某些 CLI 工具	独立存储（netsh winhttp）	netsh winhttp show proxy
环境变量	curl、wget、Git（libcurl）、Python requests 等	HTTP_PROXY / HTTPS_PROXY


第 3 步：检查网络是否能连接 GitHub
Test-NetConnection github.com -Port 443

第 4 步：通过 Git 详细日志定位故障位置
$env:GIT_CURL_VERBOSE = "1"
git ls-remote origin
GIT_CURL_VERBOSE 是一个环境变量，用于让 Git 输出底层 HTTP 客户端的详细日志
Remove-Item Env:GIT_CURL_VERBOSE：关闭当前 PowerShell 会话中的详细日志

第 4 步：找到 Windows 的代理设置
netsh winhttp show proxy
直接访问(没有代理服务器)。表示 WinHTTP 使用的是直接访问配置
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' |
Select-Object ProxyEnable, ProxyServer, AutoConfigURL
这条命令查询的是当前 Windows 用户的 Internet Settings 代理配置。

第 5 步：为什么临时设置代理后就成功了？
Test-NetConnection 127.0.0.1 -Port 7897
$env:HTTP_PROXY = "http://127.0.0.1:7897"
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
HTTP_PROXY：为支持该环境变量的程序提供 HTTP 代理地址。
HTTPS_PROXY：为支持该环境变量的程序提供 HTTPS 请求的代理地址。
http://127.0.0.1:7897：使用本机 7897 端口上的 HTTP 代理服务。
"""

"""
GitHub 连接失败：排查流程
1. 检查远程地址git remote -v
2. 检查网络连接Test-NetConnection github.com -Port 443
3. 检查代理配置
netsh winhttp show proxy
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' |
Select-Object ProxyEnable, ProxyServer, AutoConfigURL
4. 测试 Git 是否真的能访问远程仓库
git ls-remote origin
5. 最后再执行同步命令
git fetch origin
git pull origin main
"""

"""
代理软件长期使用 127.0.0.1:7897,写入 Git 的全局配置：
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897
查看：
git config --global --get http.proxy
git config --global --get https.proxy
"""

"""
网络通信
端口 = 房间号，TCP = 快递公司的送货方式
一、端口（Port）是什么
端口是一台电脑上用来区分不同网络程序的数字编号

IP 地址定位到「哪台电脑」。端口号定位到「这台电脑上的哪个程序」
IP 地址 : 端口号
192.168.1.10 : 443
└── 哪台电脑 ┘ └ 哪个程序 ┘

3. 常见端口
端口	协议/服务	说明
80	HTTP	普通网页
443	HTTPS	加密网页（你问的这个）
22	SSH	远程登录、Git 走 SSH

二、TCP 是什么
1. 核心定义
TCP 全称 Transmission Control Protocol（传输控制协议），是互联网最核心的传输层协议之一，负责可靠地把数据从一端送到另一端。
2. 它解决了什么问题
网络本身不可靠：数据包可能丢失、乱序、重复、损坏。TCP 在不可靠的网络上提供可靠传输，保证：
3. 关键机制：三次握手、四次挥手

4. TCP 和端口的关系
TCP 是传输方式。端口是 TCP 连接上的编号。
一个 TCP 连接由四元组唯一确定：(源 IP, 源端口, 目的 IP, 目的端口)


三、一张图总结层次
应用层     HTTP / HTTPS        ← 你看到的内容
            │
传输层     TCP / UDP           ← 可靠/不可靠传输，用端口区分程序
            │
网络层     IP                  ← 定位到哪台电脑
            │
链路层     以太网 / Wi-Fi       ← 物理传输

端口工作在传输层，标识程序。TCP 工作在传输层，保证可靠传输。
"""

