# 邮件发送服务

这是一个基于FastAPI和Celery的邮件发送服务，支持异步发送邮件并提供API接口。

## 项目结构

```
email_for_bubu/
├── app/                    # 主应用目录
│   ├── api/                # API路由和端点
│   ├── config/             # 配置文件
│   ├── core/               # 核心业务逻辑
│   ├── models/             # 数据模型
│   └── main.py             # 应用入口点
├── workers/                # Celery工作进程
├── email_for_bubu_env/     # Python虚拟环境
├── config.yaml             # 配置文件
├── config.yaml.example     # 配置文件示例
├── requirements.txt        # 项目依赖
├── test_email_api.py       # API测试脚本
├── test_redis.py           # Redis测试脚本
└── email.log               # 邮件发送日志
```

## 功能特性

- 基于FastAPI构建的RESTful API
- 使用Celery进行异步邮件发送
- 支持HTML和纯文本邮件
- 支持附件发送
- 邮件发送状态跟踪
- 完整的日志记录
- 配置文件管理

## 技术栈

- **FastAPI**: 现代、快速（高性能）的Web框架
- **Celery**: 分布式任务队列
- **Redis**: 消息代理和结果存储
- **SMTP**: 邮件传输协议
- **Pydantic**: 数据验证和设置管理

## 安装和配置

1. 克隆项目到本地

2. 创建并激活虚拟环境:
   ```bash
   python -m venv email_for_bubu_env
   email_for_bubu_env\Scripts\activate
   ```

3. 安装依赖:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

4. 配置邮件服务:
   - 复制`config.yaml.example`为`config.yaml`
   - 修改`config.yaml`中的SMTP服务器信息和邮箱凭证

5. 启动Redis服务器

## 启动服务

1. 启动Celery工作进程:
   ```bash
   cd workers
   python -m celery -A celery_worker worker --loglevel=info
   ```

2. 启动FastAPI应用:
   ```bash
   python app/main.py
   ```

3. API将在`http://localhost:8002`上运行

## API端点

### 发送邮件

```
POST /api/v1/send-email
```

请求体:
```json
{
  "recipients": ["recipient@example.com"],
  "subject": "邮件主题",
  "body": "邮件正文",
  "attachments": ["path/to/attachment.pdf"],
  "is_html": false,
  "sender_address": "sender@example.com",
  "sender_password": "sender_password"
}
```

### 查询任务状态

```
GET /api/v1/task-status/{task_id}
```

## 测试

运行API测试:
```bash
python test_email_api.py
```

运行Redis测试:
```bash
python test_redis.py
```

## 日志

邮件发送日志保存在`email.log`文件中，包含邮件发送成功与否的记录以及Celery任务完成状态。

## 配置

配置文件`config.yaml`包含以下设置:

```yaml
email:
  sender:
    address: "your_email@example.com"
    password: "your_email_password"
    smtp_server: "smtp.example.com"
    smtp_port: 465
  recipients:
    - "recipient1@example.com"
    - "recipient2@example.com"
```

## 许可证

本项目采用MIT许可证。