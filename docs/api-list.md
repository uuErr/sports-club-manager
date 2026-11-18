# FastAPI 接口清单

说明：
- 绝大多数接口使用 `POST` + QueryString 传参（而不是 JSON Body）。
- `token` 基本都通过 query 参数传递。
- 业务响应为 `{ "status": 整数, "data": 数据 }`。`status` 可能表示业务状态或记录数，成功值因接口而异。
- 参数列表后的 `*` 表示 FastAPI 定义为必填。其余参数有默认值，但业务逻辑仍可能要求提供，例如登录凭据和鉴权 Token。
- 路径和参数与 `python/app/api/` 中的路由定义核对。类型及默认值请查看运行后的 [Swagger UI](http://localhost:8081/docs) 或 [OpenAPI JSON](http://localhost:8081/openapi.json)。

## 会员端（/api）

### 用户（/api/user）

- POST `/api/user/login`（username, password）
- POST `/api/user/loginByEquip`（equip_id）
- POST `/api/user/verify`（token）
- POST `/api/user/password`（token, origin_pass, new_pass）
- POST `/api/user/contact`（token, origin_pass, email, phone, wechat_id）
- POST `/api/user/logout`（token）
- POST `/api/user/register`（username, password, name, card_id, phone, wechat_id, student_id, email）
- POST `/api/user/queryEquips`（token, local）
- POST `/api/user/newEquipment`（token, equip_id, name, password）
- POST `/api/user/deleteEquipment`（token, id*）
- GET `/api/user/e`（p）

### 活动/报名（/api/action）

- POST `/api/action/queryAction`（token）
- POST `/api/action/queryRecord`（token）
- POST `/api/action/queryWechatGroup`（token, record_id*）
- POST `/api/action/attendAction`（token, action_id*, borrow）
- POST `/api/action/cancelAction`（token, record_id*）

### 候补（/api/waiting）

- POST `/api/waiting/waitCreate`（token, action_id*, borrow）
- POST `/api/waiting/waitDelete`（token, waiting_id*）
- POST `/api/waiting/queryWaiting`（token）

### 名额转让（/api/transfer）

- POST `/api/transfer/queryTransfer`（token）
- POST `/api/transfer/transferRecord`（token, record_id*, receive_user）
- POST `/api/transfer/acceptTransfer`（token, transfer_id*）
- POST `/api/transfer/refuseTransfer`（token, transfer_id*）

### 工作人员（/api/staff）

- POST `/api/staff/queryAction`（token）
- POST `/api/staff/queryActionMember`（token, action_id*）
- POST `/api/staff/startSign`（token, action_id*）
- POST `/api/staff/stopAction`（token, action_id*）
- POST `/api/staff/querySign`（token, sign_code）
- POST `/api/staff/finishSign`（token, sign_code）

### 找回账号/重置密码（/api/find）

- POST `/api/find/queryUserName`（name, student_id）
- POST `/api/find/sendResetEmail`（name, student_id, username, StudentEmail）
- POST `/api/find/resetPassword`（code, password）

## 管理端（/admin/api）

### 管理员用户（/admin/api/user）

- POST `/admin/api/user/login`（username, password）
- POST `/admin/api/user/verify`（token）
- POST `/admin/api/user/password`（token, origin_pass, new_pass）
- POST `/admin/api/user/contact`（token, origin_pass, email, phone, wechat_id）
- POST `/admin/api/user/logout`（token）

### 成员管理（/admin/api/member）

- POST `/admin/api/member/queryMembers`（token, name, student_id, state, page_size, page_number）
- POST `/admin/api/member/queryReviewMembers`（token, name, student_id, page_size, page_number）
- POST `/admin/api/member/queryUnsignedMembers`（token, name, student_id, page_size, page_number）
- POST `/admin/api/member/updateUserInf`（token, id*, username, state*, name, student_id, card_id, phone, wechat_id, email）
- POST `/admin/api/member/updateUserPassword`（token, user_id*, password）
- POST `/admin/api/member/deleteUser`（token, user_id*）
- POST `/admin/api/member/passUser`（token, user_id*）
- POST `/admin/api/member/clearUserUnsigned`（token, user_id*）
- POST `/admin/api/member/resetUserUnsigned`（token, user_id*）
- POST `/admin/api/member/queryStaffMembers`（token, name, select_id）
- POST `/admin/api/member/queryInboxData`（token）

### 活动/记录管理（/admin/api/action）

- POST `/admin/api/action/create`（token, title, place, time_range, date, max_num, open_time, close_time, staff_user_id, wechat_url）
- POST `/admin/api/action/queryActions`（token, name, state, page_size, page_number）
- POST `/admin/api/action/update`（token, id*, title, place, time_range, date, max_num, open_time, close_time, staff_user_id, wechat_url）
- POST `/admin/api/action/deleteAction`（token, action_id*）
- POST `/admin/api/action/releaseAction`（token, action_id*）
- POST `/admin/api/action/stopRegisterAction`（token, action_id*）
- POST `/admin/api/action/stopAction`（token, action_id*）
- POST `/admin/api/action/reSign`（token, record_id*, sign_code）
- POST `/admin/api/action/queryActionMembers`（token, action_id*）
- POST `/admin/api/action/queryRecords`（token, name, title, page_size, page_number）
- POST `/admin/api/action/queryWorkRecords`（token, name, title, page_size, page_number）
