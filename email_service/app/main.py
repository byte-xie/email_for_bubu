"""
邮件服务主入口文件

本模块提供了一个基于FastAPI的邮件发送服务，支持发送普通文本邮件和HTML邮件。
它集成了邮件API路由，并提供了健康检查端点。

作者: [作者名]
创建日期: [创建日期]
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.api.email_api import router as email_router

app = FastAPI(title="Email Service", description="A simple email service using FastAPI", version="1.0.0")

# 注册路由
app.include_router(email_router, prefix="/api/v1", tags=["email"])

@app.get("/health")
def health_check():
    """
    健康检查端点
    
    Returns:
        dict: 包含服务状态的字典
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    import logging
    
    # 配置更详细的日志
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=8002)
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        raise