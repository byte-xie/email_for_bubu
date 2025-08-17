"""
邮件发送任务模块

本模块定义了邮件发送的Celery任务。
"""

import sys
import os

# 将项目根目录添加到Python模块搜索路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from celery import Celery
from app.core.email_service import EmailService
from app.config.settings import settings



# 创建Celery应用实例
app = Celery('email_service')

# 直接配置Celery
app.conf.broker_url = 'redis://127.0.0.1:6379/0'
app.conf.result_backend = 'redis://127.0.0.1:6379/0'

@app.task(bind=True)
def send_email_task(self, recipients: list, subject: str, body: str, attachments: list = None, is_html: bool = False, 
                  sender_address: str = None, sender_password: str = None):
    """
    发送邮件的Celery任务
    
    Args:
        recipients (list): 收件人邮箱地址列表
        subject (str): 邮件主题
        body (str): 邮件正文
        attachments (list, optional): 附件文件路径列表. Defaults to None.
        is_html (bool, optional): 是否为HTML邮件. Defaults to False.
        sender_address (str, optional): 发件人邮箱地址. Defaults to None.
        sender_password (str, optional): 发件人邮箱密码. Defaults to None.
        
    Returns:
        dict: 包含发送状态和消息的字典
    """
    try:
        # 使用配置文件中的默认发件人信息，如果未提供的话
        smtp_server = settings.sender['smtp_server']
        smtp_port = settings.sender['smtp_port']
        sender_address = sender_address or settings.sender['address']
        sender_password = sender_password or settings.sender['password']
        
        # 添加日志记录配置信息
        import logging
        from app.core.email_service import file_logger
        logger = logging.getLogger(__name__)
        logger.info(f"SMTP Config - Server: {smtp_server}, Port: {smtp_port}")
        logger.info(f"Sender Address: {sender_address}")
        
        # 创建邮件服务实例
        service = EmailService(smtp_server, smtp_port, sender_address, sender_password)
        
        # 发送邮件
        logger.info("Attempting to send email...")
        success = service.send_email(recipients, subject, body, attachments, is_html)
        logger.info(f"Email sending result: {success}")
        
        # 记录任务详情到文件日志
        file_logger.info(f"Celery task completed - To: {recipients}, Subject: {subject}, Success: {success}")
        
        if success:
            return {"status": "success", "message": "Email sent successfully"}
        else:
            return {"status": "failure", "message": "Failed to send email"}
    except Exception as exc:
        # 重试机制
        raise self.retry(exc=exc, countdown=60, max_retries=3)
    

# 测试代码
if __name__ == "__main__":
    # 从配置中获取测试数据
    test_recipients = settings.recipients
    test_subject = "来自 Celery 任务的测试邮件"
    test_body = "来自 Celery 任务的测试邮件112"
    
    # 调用send_email_task函数
    result = send_email_task(test_recipients, test_subject, test_body)
    
    # 打印发送结果
    print(f"Email sent successfully: {result}")