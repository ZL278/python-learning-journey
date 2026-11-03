"""
Git 基础
查看修改历史、恢复旧版本
git --version
git config --global user.name
git config --global user.email
--global:指定配置的作用范围:高优先级覆盖低优先级：local(默认) > global > system
git config:Git 的配置命令，用来读、写、删配置项。
git init:在当前项目中创建 Git 仓库，通常会生成一个隐藏目录 .git
git status:当前仓库的状态，例如哪些文件尚未被 Git 跟踪、哪些文件已经修改。

三个重要概念
工作区（Working Directory）
暂存区（Staging Area）
本地仓库（Repository）


理解 .gitignore 的作用:
Git 不应该追踪 .venv 目录里的文件
.gitignore 主要影响尚未被 Git 跟踪的文件。
如果某个文件之前已经被追踪，仅仅添加忽略规则并不会自动取消追踪。

.gitignore:
缓存/编译产物（__pycache__/、*.py[cod]、.pytest_cache/）：机器生成的，随时可删，下次运行自动生成。
重量级环境（.venv/、venv/）：太大，且可以通过 requirements.txt 完美复现。
敏感信息（.env）：包含密码密钥，绝对不能公开。
个人编辑器配置（.idea/）：纯属个人习惯，与代码无关

git check-ignore .venv/:检查忽略规则是否生效

git add：选择本次要保存的变更
它把文件当前的内容放进暂存区，并不创建版本记录。
git commit：创建一个版本记录
暂存区里的内容会被记录到本地 Git 仓库，之后可以查看提交历史。
"""

"""
完成第一次 Git 提交
git commit -m "Initial commit: Python learning project"
git commit：把暂存区中的文件保存为一个版本记录。
-m "..."：为这次提交写一条说明，方便以后查阅历史


git log:查看提交历史
git log --oneline:用简洁格式查看

理解 Git 状态与分支
git branch -m main:Git 的分支管理命令,move 的缩写，新的分支名


-m 和 -M 的区别：
-m / --move：重命名。如果目标名已存在，报错。
-M / --move --force：强制重命名。目标名已存在时覆盖它。
git branch -m <旧名> <新名>：重命名指定分支（可以在别的分支上操作）。
"""

"""
一个重要的工程习惯
在日常开发中，推荐养成这个顺序：
1. git status —— 检查当前状态。
2. git pull —— 同步远程更新（确认本地修改已妥善保存后）。
3. 编写或修改代码。
4. git diff —— 检查修改内容。
5. git add、git commit —— 保存本地版本。
6. git push —— 上传提交。


检查远程仓库有没有新提交
git fetch origin
"""







""""
第 1 步：理解远程仓库
git commit 只保存到本地，不会自动上传到 GitHub。
git remote -v:列出当前仓库配置的所有远程仓库（remote），并显示它们的 URL
-v:verbose(详细)

添加远程仓库
git remote add origin https://github.com/你的用户名/python-learning-journey.git

把本地代码推送到 GitHub
git push -u origin main
origin	指定 GitHub 远程仓库
main	指定要上传的本地分支
-u	建立本地分支与远程分支的跟踪关系

Git Credential Manager
git credential-manager --version

Git 清除与 github.com 对应的已保存凭据
"protocol=https`nhost=github.com`n`n" | git credential reject

指定 Git 使用浏览器授权
git push -u origin main 都要重新输入账号密码
因为你本地的 Git 没有开启“记住密码”的功能
git config --global credential.helper store
Git 会把这些信息明文保存在你电脑本地的 .gitconfig 文件里

查看修改：
git diff -- day6.py：展示尚未暂存的修改内容，不会修改文件。
按'q'推出阅读模式

练习工程化
先检查 → 再暂存 → 再提交 → 最后推送。
"""

"""
README.md
README.md 使用的是 Markdown 格式。是一种说明卡

@"
data/
todo.json
"@ | Add-Content .gitignore
@" ... "@	PowerShell 的多行字符串（Here-String）
|	管道符，把左边的字符串传给右边的命令
Add-Content	PowerShell 命令：向文件末尾追加内容（不覆盖原有内容）在末尾自动加换行
.gitignore	目标文件名
>> .gitignore	追加

检查并提交
git diff --cached
git commit -m "Update day 6 and day 7 learning notes"

推送到 GitHub
git push origin main
"""

"""
git pull
把远程仓库的更新获取下来，并整合到你当前的本地分支。
git fetch origin	获取远程更新	不会直接整合到当前分支
git pull origin main	获取并整合 main 分支更新	会

Git 日常流程
pull 拉取、add 暂存、commit 提交、push 推送
"""