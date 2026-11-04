# GitHub 使用与问题排查手册

仓库：`python-learning-journey`

本地位置：`D:\PYTHON\py2`

## 一、本次整理仓库遇到的问题

### 1. 两个本地仓库不能直接推送到同一个远程仓库

**现象：**

```text
! [rejected] main -> main (fetch first)
remote contains work that you do not have locally
```

**原因：**

`py2` 和 `py3` 分别初始化过 Git 仓库，拥有不同的提交历史。Git 无法直接把两段独立历史当成普通的更新推送。

**解决办法：**

- 选择 `py2` 作为唯一总仓库，因为它已经关联 GitHub 并保留原有历史。
- 将 `py3` 的学习文件复制到 `py2` 仓库下。
- 不复制 `py3/.git`，避免形成嵌套 Git 仓库。
- 保留原来的 `py3` 目录作为备份。

**经验：** 一个 GitHub 项目通常只需要一个 Git 仓库，不要随意把多个 `.git` 目录合并在一起。

### 2. Push 提示远程有本地没有的提交

**现象：**

```text
remote contains work that you do not have locally
```

**原因：**

GitHub 上已经有提交记录，本地没有同步远程历史。

**解决办法：**

先执行：

```powershell
git fetch origin
git log --oneline --graph --decorate --all
```

查看本地和远程的提交历史，再决定如何同步。

如果两边历史完全独立，贸然执行普通 `pull` 可能产生冲突。本次最终选择保留 `py2` 的历史，不再尝试把 `py3` 的独立历史合并进来。

**经验：** 不要为了消除报错直接使用 `git push --force`。

### 3. 文件移动后 Git 显示 deleted 和 untracked

**现象：**

```text
deleted: day1.py
untracked: py2/
```

**原因：**

文件已经从仓库根目录移动到新文件夹，但 Git 还没有记录这次变化。

**解决办法：**

```powershell
git -C .\py2 add -A
```

Git 会同时记录文件删除、新增和移动。

如果文件内容基本一致，Git 通常会识别为：

```text
renamed: day1.py -> py2/day1.py
```

**经验：** `deleted` 不一定代表文件丢失，也可能是文件移动后的正常状态。

### 4. .venv 和 .env 不应该上传

**原因：**

- `.venv` 是本地 Python 虚拟环境，体积大且与本机环境有关。
- `.env` 可能保存数据库密码、API Key 等敏感信息。

**解决办法：**

在总仓库根目录 `.gitignore` 中设置：

```gitignore
.venv/
venv/
.env
__pycache__/
*.py[cod]
.idea/
.pytest_cache/
```

本次还保留了 `py2` 和 `py3` 各自的 `.gitignore`。

注意：如果 `.env` 曾经被 Git 跟踪，仅添加忽略规则并不能自动取消跟踪。

### 5. Git 提示 LF 将转换为 CRLF

**现象：**

```text
LF will be replaced by CRLF
```

**原因：**

LF 和 CRLF 是不同操作系统常见的文本换行格式。Git 提醒文件可能发生换行符转换。

**解决办法：**

本次不需要特殊处理。只要代码正常运行，通常可以暂时忽略。

### 6. git status 显示 ahead of origin/main

**现象：**

```text
Your branch is ahead of 'origin/main' by 1 commit.
```

**原因：**

本地已经有提交，但还没有推送到 GitHub。

**解决办法：**

确认本地提交正确后：

```powershell
git push origin main
```

---

## 二、日常上传 GitHub 操作流程

以后修改 Python 代码，通常只需要以下步骤。

### 第一步：进入仓库

```powershell
cd D:\PYTHON\py2
```

### 第二步：查看修改状态

```powershell
git status
```

检查哪些文件新增、修改或删除。

### 第三步：查看具体修改内容（可选）

```powershell
git diff
```

查看尚未暂存的代码修改。

### 第四步：加入暂存区

```powershell
git add .
```

或者：

```powershell
git add -A
```

区别：

- `git add .`：加入当前目录及其子目录中的变化。
- `git add -A`：加入整个仓库的新增、修改和删除。

日常在仓库根目录操作时，两者通常都能满足需求。

### 第五步：提交版本

```powershell
git commit -m "Update Python learning notes"
```

提交信息尽量简洁，说明这次修改做了什么。

例如：

```powershell
git commit -m "Add FastAPI user update API"
```

### 第六步：推送到 GitHub

```powershell
git push origin main
```

成功后，本地提交就会同步到 GitHub。

### 第七步：检查状态

```powershell
git status
```

正常情况下：

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

表示本地没有未提交修改，并且已经与远程分支同步。

---

## 三、日常同步 GitHub 的常用命令

如果你准备在另一台电脑上继续学习，或者开始修改之前想先获取 GitHub 上的最新内容：

```powershell
git pull origin main
```

它会获取远程更新并合并到当前分支。

如果出现冲突，不要直接覆盖文件。先查看：

```powershell
git status
```

根据冲突提示处理文件，再完成提交。

---

## 四、最常用的命令速查表

| 命令                     | 作用           |
| ---------------------- | ------------ |
| `git status`           | 查看当前状态       |
| `git diff`             | 查看代码修改       |
| `git add -A`           | 暂存所有变化       |
| `git commit -m "说明"`   | 保存本地版本       |
| `git push origin main` | 上传 GitHub    |
| `git pull origin main` | 获取并合并远程更新    |
| `git fetch origin`     | 获取远程信息，不自动合并 |
| `git log --oneline`    | 查看提交历史       |
| `git remote -v`        | 查看远程仓库地址     |

## 五、这次整理后的仓库结构

```text
python-learning-journey/
├── py2/
│   ├── day1.py
│   ├── day2.py
│   ├── day3.py
│   ├── day4.py
│   ├── day5.py
│   ├── day6.py
│   ├── day7.py
│   ├── test.py
│   └── .gitignore
│
├── py3/
│   ├── app/
│   ├── w4learn/
│   ├── .gitignore
│   ├── README.md
│   └── requirements.txt
│
├── .gitignore
├── README.md
└── requirements.txt
```

原来的 `D:\PYTHON\py3` 本地目录暂时保留作为备份。

---

**最后记住日常上传的核心流程：**

```text
修改代码
   ↓
git status
   ↓
git add -A
   ↓
git commit -m "修改说明"
   ↓
git push origin main
   ↓
上传完成
```

遇到问题时，先看报错，再看 `git status`，不要盲目使用强制推送或删除 Git 文件夹。
