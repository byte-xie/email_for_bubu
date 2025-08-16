"""
邮件数据模型定义模块

本模块定义了邮件发送请求的数据模型，用于验证和序列化API请求数据。
"""
import sys
import os
from pydantic import BaseModel
from typing import List, Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 导入配置文件中的邮箱和授权码信息
from app.config.settings import settings

class EmailRequest(BaseModel):
    """
    邮件请求数据模型
    
    该模型定义了发送邮件API所需的数据结构，包括收件人、主题、正文等字段。
    """
    recipients: List[str]  # 收件人邮箱列表
    subject: str           # 邮件主题
    body: str              # 邮件正文
    attachments: Optional[List[str]] = None  # 附件文件路径列表
    is_html: Optional[bool] = False          # 是否为HTML邮件，默认为False
    sender_address: Optional[str] = None     # 发件人邮箱地址，如果传了，就覆盖配置文件
    sender_password: Optional[str] = None    # 发件人邮箱密码，如果传了，就覆盖配置文件


# 测试代码
if __name__ == "__main__":
    
    # 创建一个示例EmailRequest实例来验证模型
    example_request = EmailRequest(
        recipients=settings.recipients,
        subject="测试邮件",
        body="这是一封测试邮件。",
        attachments=None,
        is_html=False,
        sender_address=settings.sender.get('address'),
        sender_password=settings.sender.get('password')
    )
    print("测试EmailRequest模型:")
    print(f"收件人: {example_request.recipients}")
    print(f"主题: {example_request.subject}")
    print(f"正文: {example_request.body}")
    print(f"发件人地址: {example_request.sender_address}")
    print(f"SMTP服务器信息已配置")
    print("模型验证通过")