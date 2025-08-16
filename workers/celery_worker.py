"""
Celery工作进程配置文件

本模块配置了Celery应用，用于处理异步邮件发送任务。
"""
import os
import sys
from celery import Celery

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 创建Celery应用实例
app = Celery('email_service')

# 确保任务被正确导入
from app.core.email_tasks import send_email_task

# 配置Celery
app.conf.update(
    # 使用Redis作为消息代理
    broker_url='redis://127.0.0.1:6379/0',
    
    # 使用Redis作为结果后端
    result_backend='redis://127.0.0.1:6379/0',
    
    # 任务序列化方式
    task_serializer='json',
    
    # 结果序列化方式
    result_serializer='json',
    
    # 接受的内容类型
    accept_content=['json'],
    
    # 时区设置
    timezone='Asia/Shanghai',
    
    # 启用UTC时间
    enable_utc=True,
    
    # 任务路由
task_routes={
    'app.core.email_tasks.send_email_task': {'queue': 'email_queue'},
},

# Windows兼容性设置
worker_pool = 'solo',
)

# 手动注册任务
app.tasks.register(send_email_task)

# 自动发现任务
import logging

# 简单的日志配置
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.info("Starting task autodiscovery...")
app.autodiscover_tasks(['app.core'])
logger.info("Task autodiscovery completed.")

if __name__ == '__main__':
    app.start()