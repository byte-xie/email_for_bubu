import sys
import os

# 将项目根目录添加到Python模块搜索路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import textwrap

# 简化的文件日志记录器配置
file_logger = logging.getLogger('email_file_logger')
file_logger.setLevel(logging.INFO)

# 简单的文件处理器配置
log_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'email.log')
file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 创建格式化器并添加到处理器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

file_logger.addHandler(file_handler)

class EmailService:
    """
    邮件服务类
    
    该类提供了发送邮件的功能，支持普通文本邮件和HTML邮件，
    以及添加附件的功能。
    """
    
    def __init__(self, smtp_server: str, smtp_port: int, sender_address: str, sender_password: str):
        """
        初始化邮件服务
        
        Args:
            smtp_server (str): SMTP服务器地址
            smtp_port (int): SMTP服务器端口
            sender_address (str): 发件人邮箱地址
            sender_password (str): 发件人邮箱密码
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_address = sender_address
        self.sender_password = sender_password
        self.logger = logging.getLogger(__name__)
    
    def send_email(self, recipients: list, subject: str, body: str, attachments: list = None, is_html: bool = False) -> bool:
        """
        发送邮件
        
        该方法构建邮件内容并发送给指定收件人。
        
        Args:
            recipients (list): 收件人邮箱地址列表
            subject (str): 邮件主题
            body (str): 邮件正文
            attachments (list, optional): 附件文件路径列表. Defaults to None.
            is_html (bool, optional): 是否为HTML邮件. Defaults to False.
            
        Returns:
            bool: 发送成功返回True，否则返回False
        """
        try:
            self.logger.info(f"Starting to send email to {recipients}")
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = self.sender_address
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            # 添加邮件正文
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # 添加附件
            if attachments:
                for file_path in attachments:
                    if os.path.isfile(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
            
            # 连接SMTP服务器并发送邮件
            self.logger.info(f"Connecting to SMTP server {self.smtp_server}:{self.smtp_port}")
            try:
                # 使用SSL连接SMTP服务器
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
                self.logger.info("SMTP SSL connection established")
            except Exception as e:
                self.logger.error(f"Failed to connect to SMTP server: {e}", exc_info=True)
                raise
            
            self.logger.info("Logging in to SMTP server")
            try:
                server.login(self.sender_address, self.sender_password)
                self.logger.info("Login successful")
            except Exception as e:
                self.logger.error(f"Failed to login: {e}", exc_info=True)
                raise
            
            self.logger.info("Sending email")
            try:
                text = msg.as_string()
                server.sendmail(self.sender_address, recipients, text)
                self.logger.info("Email sent successfully")
            except Exception as e:
                self.logger.error(f"Failed to send email: {e}", exc_info=True)
                raise
            
            self.logger.info("Quitting SMTP server")
            server.quit()
            
            # 记录邮件详情
            self._log_email_details(recipients, subject, body, is_html)
            self.logger.info("Email sent successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error sending email: {e}", exc_info=True)
            return False
    
    def _log_email_details(self, recipients: list, subject: str, body: str, is_html: bool = False):
        """
        记录邮件发送详情
        
        Args:
            recipients (list): 收件人列表
            subject (str): 邮件主题
            body (str): 邮件正文
            is_html (bool): 是否为HTML邮件
        """
        # 对HTML邮件正文进行格式化处理，避免日志中显示为单行长文本
        if is_html:
            # 使用textwrap库处理长文本换行
            wrapped_body = textwrap.fill(body.replace('\n', ''), width=100, break_long_words=False, break_on_hyphens=False)
            body_preview = wrapped_body[:500]  # 只记录前500个字符
        else:
            body_preview = body[:200]  # 对普通文本邮件只记录前200个字符
        
        # 记录到控制台
        self.logger.info(f"Email sent - To: {recipients}, Subject: {subject}, Body preview: {body_preview}")
        
        # 使用文件日志记录器记录邮件详情
        file_logger.info(f"Email sent - Sender: {self.sender_address}, To: {recipients}, Subject: {subject}")


# 测试代码
if __name__ == "__main__":
    # 导入配置
    from app.config.settings import settings
    
    # 创建EmailService实例
    email_service = EmailService(
        smtp_server=settings.sender.get('smtp_server'),
        smtp_port=settings.sender.get('smtp_port'),
        sender_address=settings.sender.get('address'),
        sender_password=settings.sender.get('password')
    )
    
    # 调用send_email方法
    success = email_service.send_email(
        recipients=settings.recipients,
        subject="Test Email",
        body="这是从 EmailService 类发送的测试邮件"
    )
    
    # 打印发送结果
    print(f"Email sent successfully: {success}")