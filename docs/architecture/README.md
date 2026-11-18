# 系统架构与流程图

系统由会员端（含工作人员页面）、管理端、Python FastAPI 后端及数据库组成。通过 SQLAlchemy 连接 MySQL 或 SQLite，找回密码时调用 SMTP 邮件服务。

| 文件 | 内容 | 对应代码 |
|---|---|---|
| [context.puml](context.puml) | 系统边界、三类用户和外部邮件服务 | `python/app/main.py` |
| [components.puml](components.puml) | 前端、后端路由、数据库与邮件模块的组件关系 | 两端 `src/`、`python/app/api/`、`python/app/db.py` |
| [reset-password.puml](reset-password.puml) | 身份验证、邮箱选择、验证码与密码重置流程 | `python/app/api/find.py`、`python/app/email_service.py` |

MySQL 表结构在 `database/install.sql`，SQLite 初始化结构在 `python/app/db_schema.py`。Docker 默认使用 MySQL，一键启动脚本使用 SQLite。

`.puml` 是 PlantUML 图源文件，不参与应用运行。可使用支持 PlantUML 的编辑器扩展预览并导出 SVG/PNG，渲染环境按所用扩展配置。
