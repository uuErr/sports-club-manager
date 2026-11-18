# 项目文档

| 文档 | 内容 |
|---|---|
| [接口清单](api-list.md) | 会员、工作人员和管理员接口的路径及查询参数 |
| [运行与整合说明](integration/前端+Python后端整合说明.md) | Docker 部署、本地开发、数据库与 SMTP 配置、前端代理 |
| [系统架构与流程图](architecture/README.md) | 系统边界、组件结构和找回密码流程的 PlantUML 图源 |

当前后端为 `python/` 下的 FastAPI 应用。Docker 默认使用 MySQL，一键启动脚本使用 SQLite。

后端启动后，可访问 [Swagger UI](http://localhost:8081/docs) 查看接口定义，或读取 [OpenAPI JSON](http://localhost:8081/openapi.json)。
