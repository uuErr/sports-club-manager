# 🏸 Sports Club Manager / 体育俱乐部管理系统

<p align="center">
  <b>Member & Event Management System<br>会员与活动管理系统</b><br><br>
  <br>
  <img src="https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/fastapi-0.115-009688.svg?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/vue-3.x-4FC08D.svg?style=flat-square&logo=vue.js&logoColor=white" alt="Vue 3">
  <br>
  <img src="https://img.shields.io/badge/database-SQLite_|_MySQL-4479A1.svg?style=flat-square&logo=mysql&logoColor=white" alt="SQLite / MySQL">
  <img src="https://img.shields.io/badge/deploy-Docker_|_Bare_Metal-2496ED.svg?style=flat-square&logo=docker&logoColor=white" alt="Docker / Bare Metal">
  <img src="https://img.shields.io/badge/testing-pytest-0A9EDC.svg?style=flat-square&logo=pytest&logoColor=white" alt="pytest">
</p>

<p align="center">
  <b>Member registration · Event booking · Waitlist · QR-Code check-in · Admin dashboard<br>会员注册 · 活动预约 · 候补队列 · 扫码签到 · 管理后台</b><br>
  <sub>Clone → Configure → Deploy. No separate database service needed in SQLite mode.<br>克隆 → 配置 → 部署。SQLite 模式无需独立数据库服务。</sub>
</p>

---

## 📖 Table of Contents / 目录

- [What is this? / 这是什么？](#-what-is-this--这是什么)
- [Who is this for? / 谁适合用？](#-who-is-this-for--谁适合用)
- [Features / 功能](#-features--功能)
- [Quick Start / 快速开始](#-quick-start--快速开始)
- [Demo Mode / 演示数据](#-demo-mode--演示数据)
- [Make It Yours / 定制你的系统](#-make-it-yours--定制你的系统)
- [Architecture / 架构](#-architecture--架构)
- [API Overview / API 概览](#-api-overview--api-概览)
- [Deployment / 部署](#-deployment--部署)
- [Tech Stack / 技术栈](#-tech-stack--技术栈)
- [Testing / 测试](#-testing--测试)
- [Security / 安全](#-security--安全)
- [Roadmap / 路线图](#-roadmap--路线图)
- [Contributing / 贡献](#-contributing--贡献)

---

## 💡 What is this? / 这是什么？

**English:** A full-stack club management web application that handles member registration, event booking, waitlist queuing, QR-code attendance, and admin dashboards. Designed to be customized — change the name, logo, and labels to fit your club.

**中文：** 一个全栈的俱乐部管理 Web 应用，涵盖会员注册、活动预约、候补队列、扫码签到、管理后台等功能。设计为可定制化——修改名称、Logo、标签即可适配你的俱乐部。

---

## 🎯 Who is this for? / 谁适合用？

| You are… / 你是… | You can… / 你可以… |
|---|---|
| 🎓 University club officer / 大学社团负责人 | Manage member signups & event attendance / 管理成员报名和活动出勤 |
| 🏋️ Community sports center / 社区体育中心 | Track class bookings with waitlist / 带候补的课程预约管理 |
| 💻 Full-stack learner / 全栈学习者 | Study a complete Vue + FastAPI project / 学习完整的 Vue + FastAPI 项目 |
| 🏫 CS student / 计算机专业学生 | Use as reference or base project / 作为参考或毕设基础 |
| 🔧 Hobbyist / 爱好者 | Self-host a free management tool / 自托管免费管理工具 |

---

## ✨ Features / 功能

### Member Portal / 会员端 (Vue 3 + Vant UI)

| English | 中文 |
|---|---|
| 📝 Register with email, phone, member ID | 📝 邮箱/手机/学号注册 |
| 🔑 Login via password or one-tap equipment | 🔑 密码登录或一键设备登录 |
| 📅 Browse & register for events | 📅 浏览并报名活动 |
| ⏳ Auto waitlist when full | ⏳ 满员自动进入候补 |
| ↔️ Transfer spot to another member | ↔️ 名额转让给其他成员 |
| 📱 QR-code attendance scanning | 📱 扫码签到 |
| 🔍 Account recovery & password reset | 🔍 找回账号与重置密码 |

### Admin Dashboard / 管理端 (Vue 3 + LayUI)

| English | 中文 |
|---|---|
| 👥 Member CRUD, approve, reset password | 👥 成员增删改查、审核、重置密码 |
| 📊 Inbox stats dashboard | 📊 首页统计面板 |
| 🏟 Event create, release, stop, assign staff | 🏟 活动创建、发布、停止、分配工作人员 |
| 📋 Booking & attendance records | 📋 预约与出勤记录查询 |
| ⚠️ No-show tracking & auto-restriction | ⚠️ 失信追踪与自动限制 |

### Backend / 后端 (FastAPI)

| English | 中文 |
|---|---|
| 🗄️ Dual database: SQLite (dev) + MySQL (prod) | 🗄️ 双数据库：SQLite（开发）+ MySQL（生产） |
| 📧 SMTP email with HTML template | 📧 SMTP 邮件，可自定义 HTML 模板 |
| 🔐 UUID token auth with expiry | 🔐 UUID 令牌认证，含过期机制 |
| 🌐 CORS middleware | 🌐 跨域中间件（当前允许所有来源） |
| 🧪 pytest suite with SQLite integration tests | 🧪 pytest 测试套件，SQLite 集成测试 |

---

## ⚡ Quick Start / 快速开始

```bash
# Download this repository and open a terminal in its root directory.
# 下载当前仓库后，在项目根目录打开终端。

# Windows
.\start.ps1

# macOS / Linux
bash start.sh
```

→ Open / 打开 <http://localhost:8081/docs> — backend live with SQLite.  
→ Fresh-install admin / 首次初始化管理员: `admin` / `admin`（登录后修改；已有数据库的密码不会自动重置）

**Requirements / 环境要求:** Python 3.10+. That's it. No Docker, MySQL, or Node.js needed.

---

## 🎬 Demo Mode / 演示数据

```bash
# Fill database with sample data / 填充演示数据
DB_TYPE=sqlite .venv/bin/python python/seed_demo.py  # macOS / Linux
```

Windows PowerShell（项目根目录）：

```powershell
$env:DB_TYPE = "sqlite"
.venv\Scripts\python python/seed_demo.py
```

Creates 6 members (password: `Aa1$abcd`), 3 events, and bookings.  
创建 6 个会员（密码 `Aa1$abcd`）、3 个活动和预约记录。

---

## 🎨 Make It Yours / 定制你的系统

**Step 1 — Configure branding / 配置品牌信息** (`python/.env`):

```env
APP_NAME="My Badminton Club"
ORG_NAME="My Badminton Club"
MEMBER_ID_LABEL="Student ID"        # or "Employee ID", "Member #"
EMAIL_DOMAIN="student.uni.edu"      # optional, for auto-generated emails
```

**Step 2 — Replace UI text / 替换界面文字:**  
Search `体育俱乐部` in the frontend and replace with your club name.  
在前端搜索 `体育俱乐部` 并替换为你的俱乐部名称。

**Step 3 — Replace logos / 替换 Logo:**  
- `admin-front-end/public/favicon.svg` and `favicon.ico`
- `client-front-end/public/favicon.svg` and `favicon.ico`

**Step 4 — Configure URLs / 配置 URL** (`admin-front-end/public/config.js`)

---

## 🏗 Architecture / 架构

```
Browser / 浏览器
  ├─ Member Portal (:8080) ─── /api/* ─────┐
  └─ Admin Dashboard (:8082) ─ /admin/api/* ─┤
                                             ▼
                                    FastAPI Backend (:8081)
                                    ├─ Auth (token-based)
                                    ├─ Booking + Waitlist
                                    ├─ Transfer Engine
                                    ├─ QR Sign-in
                                    └─ Admin CRUD
                                             │
                                    SQLAlchemy (SQL + transactions)
                                    ├─ SQLite (dev 开发)
                                    └─ MySQL 8 (prod 生产)
```

---

## 📮 API Overview / API 概览

Most endpoints: `POST` + QueryString → `{ "status": int, "data": ... }`  
多数接口使用 `POST` + QueryString 传参，另有 GET `/api/user/e`。

| Prefix / 前缀 | Module / 模块 | Examples / 示例 |
|---|---|---|
| `/api/user` | Member Account / 会员账户 | login, register, verify, password, equipment |
| `/api/action` | Events & Booking / 活动与预约 | queryAction, attendAction, cancelAction |
| `/api/waiting` | Waitlist / 候补 | waitCreate, waitDelete, queryWaiting |
| `/api/transfer` | Spot Transfer / 名额转让 | queryTransfer, transferRecord, acceptTransfer |
| `/api/staff` | Check-in / 签到 | queryAction, startSign, querySign, finishSign |
| `/api/find` | Account Recovery / 账号找回 | queryUserName, sendResetEmail, resetPassword |
| `/admin/api/*` | Admin Panel / 管理后台 | member CRUD, event CRUD, inbox stats |

📄 Full list / 完整清单: [`docs/api-list.md`](docs/api-list.md)  
🧪 Interactive docs / 交互文档: <http://localhost:8081/docs>  
📚 Documentation / 项目文档: [`docs/README.md`](docs/README.md)

---

## 🚢 Deployment / 部署

### Option A: Docker (full stack / 全家桶)

首次启动前，复制根目录 `.env.example` 为 `.env`，设置 `MYSQL_ROOT_PASSWORD`。Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

macOS / Linux：`cp .env.example .env`。已有 `.env` 时直接编辑。已有 MySQL 数据卷须使用原密码，修改 `.env` 不会修改数据库中已有的密码。

然后在项目根目录启动：

```bash
docker compose up --build -d
```

Launches MySQL + backend + member portal + admin dashboard.  
启动 MySQL + 后端 + 会员端 + 管理端。

本地开发、端口和配置位置详见[运行与整合说明](docs/integration/前端+Python后端整合说明.md)。

### Option B: Bare metal / 裸机部署

```bash
# Backend / 后端
cd python
pip install -r requirements.txt
cp .env.example .env  # SQLite configuration; adjust for MySQL if needed
uvicorn app.main:app --host 0.0.0.0 --port 8081

# Frontend / 前端 (separate terminals / 分开终端)
cd admin-front-end && npm install && npm run build
cd client-front-end && npm install && npm run build
# Serve dist/ with Nginx / 用 Nginx 托管 dist/
```

### Option C: Cloud / 云部署 (Render / Railway / VPS)

1. Set `DB_TYPE=sqlite` for simple single-server / 单服务器用 SQLite
2. Or point `DB_HOST` to managed MySQL / 或指向云端 MySQL
3. Frontends are static — deploy to CDN / 前端是静态文件，可部署到 CDN

---

## 🛠 Tech Stack / 技术栈

| Layer / 层 | Technology / 技术 |
|---|---|
| Backend / 后端框架 | FastAPI 0.115 (Python 3.10+) |
| Database access / 数据访问 | SQLAlchemy 2.0 (SQL + transactions / SQL 与事务) |
| Databases / 数据库 | SQLite (dev) / MySQL 8 (prod) |
| Member UI / 会员端 | Vue 3 + Vant UI 4 |
| Admin UI / 管理端 | Vue 3 + LayUI Vue 2 |
| Auth / 认证 | UUID tokens (3-hour session / 3 小时有效期) |
| Email / 邮件 | SMTP with STARTTLS (port 587) |
| Testing / 测试 | pytest + httpx + SQLite |
| Container / 容器 | Docker + docker-compose |
| Reverse proxy / 反代 | Nginx (Alpine) |

---

## 🧪 Testing / 测试

```bash
pip install -r python/requirements.txt
pip install pytest httpx
# macOS / Linux, from project root
PYTHONPATH=python pytest tests/ -v
```

Windows PowerShell（项目根目录）：

```powershell
$env:PYTHONPATH = "python"
pytest tests/ -v
```

Tests cover token verification, login, registration, password validation, utilities. Integration tests use temporary SQLite files.  
测试覆盖令牌验证、登录、注册、密码校验、工具函数。集成测试使用临时 SQLite 数据库文件。

---

## 🔒 Security / 安全

| Concern / 关注点 | Implementation / 实现 | Production Note / 生产环境建议 |
|---|---|---|
| Password hashing / 密码哈希 | MD5 + salt | ⚠️ Migrate to bcrypt/argon2 / 迁移到 bcrypt |
| Auth / 认证 | UUID v4 token, 3h expiry | Add JWT + refresh tokens / 加入 JWT |
| CORS | Open (`*`) | Restrict to your domain / 限制为你的域名 |
| SMTP | STARTTLS on port 587 | Use app-specific passwords |
| SQL injection / SQL 注入 | Parameterized queries / 参数化查询 | ✅ Safe / 安全 |

---

## 🗺️ Roadmap / 路线图

- [ ] 🌐 i18n / Internationalization / 国际化（英文界面）
- [ ] 🔐 bcrypt/argon2 password migration / 密码哈希迁移
- [ ] 🔑 JWT authentication with refresh tokens / JWT 认证
- [ ] 📊 Advanced statistics & charts dashboard / 高级统计图表看板
- [ ] 📱 PWA support / PWA 移动端支持
- [ ] 🔔 WebSocket real-time waitlist notifications / WebSocket 实时候补通知
- [ ] 📧 Email notification system / 邮件通知系统
- [ ] 🧪 Frontend e2e tests (Playwright/Cypress) / 前端端到端测试
- [ ] 🐳 One-click Docker deployment to cloud / 一键云部署

---

## 🤝 Contributing / 贡献

Pull requests welcome! See [`CONTRIBUTING.md`](CONTRIBUTING.md).  
欢迎提交 PR！详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。


<p align="center">
  <sub>Built with ❤️ for clubs everywhere. Clone it. Customize it. Share it.<br>为所有俱乐部而建。克隆、定制、分享。</sub>
</p>
