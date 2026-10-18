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
"""

