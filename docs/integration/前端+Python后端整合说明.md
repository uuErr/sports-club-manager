# 前端与 Python 后端运行说明

项目由会员端、管理端、FastAPI 后端及数据库组成。默认 Docker 配置使用 Python 后端和 MySQL 8.0；一键启动脚本使用 SQLite，仅启动后端。

## Docker：运行完整系统

首次运行时，复制根目录 `.env.example` 为 `.env` 并设置 `MYSQL_ROOT_PASSWORD`：

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

macOS / Linux 使用 `cp .env.example .env`。已有 `.env` 时直接编辑，不要覆盖。

新建数据库可设置自选密码；已有 MySQL 数据卷必须填写原密码，修改 `.env` 不会更新数据库内部密码。`.env` 已被 Git 忽略，不应上传。

然后在项目根目录执行：

```bash
docker compose up --build -d
docker compose ps
```

| 服务 | 地址 | 说明 |
|---|---|---|
| 会员端 | http://localhost:8080 | Vue 3 + Vant，由 Nginx 托管 |
| 管理端 | http://localhost:8082 | Vue 3 + LayUI Vue，由 Nginx 托管 |
| 后端文档 | http://localhost:8081/docs | FastAPI 交互文档 |
| MySQL | localhost:3306 | 数据库名 `badminton1` |

`docker-compose.yml` 定义上述四个服务，后端服务名为 `backend`。首次创建 MySQL 数据卷时，执行 `database/install.sql` 初始化数据库；已有数据卷不会重复执行。首次初始化的管理员为 `admin` / `admin`，登录后请修改密码。已有数据库中的账号密码不会被此次代码更新自动重置。

### 本机开发覆盖配置

使用镜像源版本的 Python 基础镜像，并将服务端口仅绑定本机：

```bash
docker compose -f docker-compose.yml -f compose.local.yaml up --build -d
```

此配置固定 Compose 项目名为 `sports-club-local`，以复用本机已有容器及数据库卷。MySQL 主机端口为 `13306`，应用端口仍为 `8080`、`8081`、`8082`。覆盖文件使用 `!override` 标签，需要支持该标签的 Docker Compose 版本。

### 日志和停止

```bash
docker compose logs --tail=100 backend
docker compose down
```

使用覆盖配置启动时，后续命令也应带上相同的两个 `-f` 参数。普通 `down` 保留 MySQL 数据卷。

## 本地开发：SQLite 后端与两个前端

需要 Python 3.10+；运行前端还需 Node.js 和 npm。

在项目根目录启动后端：

```powershell
# Windows PowerShell
.\start.ps1
```

```bash
# macOS / Linux
bash start.sh
```

脚本创建 `.venv`、安装 `python/requirements.txt`，设置 `DB_TYPE=sqlite` 并在 `8081` 端口启动后端。SQLite 文件为项目根目录的 `badminton.db`，首次启动会自动创建表、视图及基础账号。

分别在两个新终端启动前端：

```bash
cd client-front-end
npm ci
npm run serve
```

```bash
cd admin-front-end
npm ci
npm run serve
```

会员端为 `8080`，管理端为 `8082`。开发代理配置位于各自的 `vue.config.js`，后端目标为 `127.0.0.1:8081`。Docker 与本地运行默认使用相同的应用端口，应选择一种方式以避免端口冲突。

## 数据库与 SMTP 配置

本地手动运行时，将 `python/.env.example` 复制为 `python/.env` 后调整配置。后端从 `python/.env` 读取配置，进程环境变量优先。

- `DB_TYPE=sqlite`：无需独立数据库服务。一键启动脚本固定使用此模式。
- `DB_TYPE=mysql`：同时设置 `DB_HOST`、`DB_PORT`、`DB_NAME`、`DB_USER`、`DB_PASSWORD`，提前导入 `database/install.sql`。直接运行且没有配置时，代码默认使用 MySQL。
- 邮件找回密码需要 `SMTP_HOST`、`SMTP_PORT`、`SMTP_USER`、`SMTP_PASSWORD`，可选 `SMTP_FROM`。端口 `587` 时启用 STARTTLS。未配置或发送失败时返回 `Email Error`。
- `EMAIL_DOMAIN` 用于按会员编号拼接邮箱。传入 `StudentEmail` 参数时使用此逻辑；不传时使用账号登记的邮箱。未配置域名时，代码回退到 `example.com`，实际使用时应配置有效域名。

**Docker 的配置位置：** 后端镜像不包含 `python/.env`。Compose 从根目录 `.env` 读取配置，并显式传入数据库、SMTP、应用名称、组织名称和邮箱域名；配置项见根目录 `.env.example`。MySQL 初始化与后端连接共用 `MYSQL_ROOT_PASSWORD`，数据库名共用 `MYSQL_DATABASE`。本地直接运行 Python 时仍使用 `python/.env`。

## 前后端请求链路

| 前端 | 请求前缀 | Docker Nginx 代理目标 |
|---|---|---|
| 会员端 | `/api` | `http://backend:8081`，保留路径 |
| 管理端 | `/admin/api` | `http://backend:8081`，保留路径 |

两端 Nginx 配置均在各自目录的 `nginx.conf`。若将静态构建产物部署到其他服务器，也需配置 API 反向代理和单页应用路由回退。

接口多数使用 `POST` + 查询参数，登录后通过查询参数传递 UUID Token。响应为 `{ "status": 整数, "data": 数据 }`，具体状态含义依接口而异。

路径与参数见 [接口清单](../api-list.md)，实际类型、默认值和必填项见运行后的 [交互文档](http://localhost:8081/docs)。
