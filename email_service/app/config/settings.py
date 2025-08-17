"""
邮件服务配置模块

本模块定义了邮件服务的配置类，用于读取和管理邮件服务所需的配置信息。
"""
import yaml
import os

class EmailSettings:
    """
    邮件配置类
    
    该类用于加载和存储邮件服务的配置信息，包括SMTP服务器信息和发件人信息。
    """
    
    def __init__(self, config_file: str = "config.yaml"):
        """
        初始化邮件配置
        
        Args:
            config_file (str, optional): 配置文件路径. Defaults to "config.yaml".
        """
        # 获取项目根目录下的配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), config_file)
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        self.sender = config['email']['sender']
        self.recipients = config['email']['recipients']
        # 未来支持多发件邮箱池
        self.senders = config['email'].get('senders', [])
        
        # 未来支持收件人分组
        self.recipients_group = config['email'].get('recipients_group', {})

# 全局设置实例
settings = EmailSettings()

# 测试代码
if __name__ == "__main__":
    print("测试配置加载功能:")
    print(f"发件人地址: {settings.sender.get('address', '未设置')}")
    print(f"SMTP服务器: {settings.sender.get('smtp_server', '未设置')}")
    print(f"收件人列表: {settings.recipients}")
    print("配置加载测试完成")