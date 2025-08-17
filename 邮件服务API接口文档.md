# 邮件服务API接口文档

## 概述

本API文档详细描述了邮件服务提供的RESTful API接口。该服务基于FastAPI构建，支持异步发送邮件，并提供任务状态查询功能。

## 基础URL

```
http://localhost:8002/api/v1
```

## 状态码定义

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 400 | Bad Request | 请求参数错误 |
| 404 | Not Found | 请求的资源不存在 |
| 422 | Unprocessable Entity | 请求体格式正确，但语义错误 |
| 500 | Internal Server Error | 服务器内部错误 |
| 503 | Service Unavailable | 服务暂时不可用 |

## API接口

### 1. 发送邮件

#### 接口地址
```
POST /send-email
```

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| recipients | array[string] | 是 | 收件人邮箱地址列表 |
| subject | string | 是 | 邮件主题 |
| body | string | 是 | 邮件正文 |
| attachments | array[string] | 否 | 附件文件路径列表 |
| is_html | boolean | 否 | 是否为HTML邮件，默认为false |
| sender_address | string | 否 | 发件人邮箱地址，如果提供将覆盖配置文件中的设置 |
| sender_password | string | 否 | 发件人邮箱密码，如果提供将覆盖配置文件中的设置 |

#### 请求示例

```json
{
  "recipients": ["recipient@example.com"],
  "subject": "测试邮件",
  "body": "这是一封测试邮件。",
  "attachments": ["/path/to/attachment.pdf"],
  "is_html": false,
  "sender_address": "sender@example.com",
  "sender_password": "sender_password"
}
```

#### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| status | string | 任务状态，固定为"queued" |
| message | string | 响应消息 |
| task_id | string | 任务ID，用于查询任务状态 |

#### 响应示例

```json
{
  "status": "queued",
  "message": "Email task queued successfully",
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 状态码说明

| 状态码 | 场景 | 具体含义 |
|--------|------|----------|
| 200 | 成功提交任务 | 邮件发送任务已成功加入队列 |
| 422 | 参数验证失败 | 请求体中的参数不符合要求，如缺少必填字段或字段类型错误 |
| 500 | 服务器内部错误 | 任务队列服务不可用或配置错误 |

### 2. 查询任务状态

#### 接口地址
```
GET /task-status/{task_id}
```

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| task_id | string | 是 | 任务ID |

#### 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| state | string | 任务状态，可能值：PENDING, SUCCESS, FAILURE |
| status | string | 任务状态描述 |
| result | string | 任务执行结果（仅在任务成功时返回） |

#### 响应示例

任务等待执行：
```json
{
  "state": "PENDING",
  "status": "Task is waiting to be processed"
}
```

任务执行成功：
```json
{
  "state": "SUCCESS",
  "status": "success",
  "result": {
    "status": "success",
    "message": "Email sent successfully"
  }
}
```

任务执行失败：
```json
{
  "state": "FAILURE",
  "status": "ConnectionError('Failed to connect to SMTP server')"
}
```

#### 状态码说明

| 状态码 | 场景 | 具体含义 |
|--------|------|----------|
| 200 | 成功查询 | 成功返回任务状态信息 |
| 404 | 任务不存在 | 指定的任务ID不存在 |
| 500 | 服务器内部错误 | 查询任务状态时发生内部错误 |

## 任务状态说明

1. **PENDING**: 任务已提交但尚未被worker处理
2. **SUCCESS**: 任务已成功执行
3. **FAILURE**: 任务执行失败

## 错误处理

当API调用发生错误时，将返回包含错误信息的JSON响应：

```json
{
  "detail": "错误描述信息"
}
```

## 使用示例

### 发送普通文本邮件

```bash
curl -X POST "http://localhost:8002/api/v1/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": ["recipient@example.com"],
    "subject": "测试邮件",
    "body": "这是一封测试邮件。"
  }'
```

### 发送HTML邮件

```bash
curl -X POST "http://localhost:8002/api/v1/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": ["recipient@example.com"],
    "subject": "HTML测试邮件",
    "body": "<h1>这是一封HTML测试邮件</h1><p>包含HTML格式的内容。</p>",
    "is_html": true
  }'
```

### 查询任务状态

```bash
curl -X GET "http://localhost:8002/api/v1/task-status/550e8400-e29b-41d4-a716-446655440000"
```