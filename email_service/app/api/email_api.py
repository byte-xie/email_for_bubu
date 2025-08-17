import sys
import os
import logging
from fastapi import APIRouter, HTTPException

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.email_models import EmailRequest
from app.config.settings import settings
# 导入Celery任务
from app.core.email_tasks import send_email_task

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/send-email")
def send_email(request: EmailRequest):
    """
    发送邮件接口
    
    该接口接收邮件请求参数，调用邮件服务发送邮件，并返回发送结果。
    
    Args:
        request (EmailRequest): 包含邮件发送所需信息的请求体
        
    Returns:
        dict: 包含发送状态和消息的字典
        
    Raises:
        HTTPException: 当邮件发送失败时抛出500错误
    """
    try:
        logger.info(f"Received email request: recipients={request.recipients}, subject=\"{request.subject}\"")
        
        # 发送Celery任务而不是直接发送邮件
        task = send_email_task.delay(
            recipients=request.recipients,
            subject=request.subject,
            body=request.body,
            attachments=request.attachments,
            is_html=request.is_html,
            sender_address=request.sender_address,
            sender_password=request.sender_password
        )
        
        logger.info(f"Email task queued with ID: {task.id}")
        return {"status": "queued", "message": "Email task queued successfully", "task_id": task.id}
    except Exception as e:
        logger.error(f"Failed to queue email task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    """
    获取邮件发送任务状态
    
    Args:
        task_id (str): 任务ID
        
    Returns:
        dict: 包含任务状态信息的字典
    """
    try:
        # 获取任务结果
        task = send_email_task.AsyncResult(task_id)
        
        # 根据任务状态返回相应信息
        if task.state == 'PENDING':
            # 任务正在等待执行
            response = {
                'state': task.state,
                'status': 'Task is waiting to be processed'
            }
        elif task.state != 'FAILURE':
            # 任务已完成或正在执行
            response = {
                'state': task.state,
                'status': task.info.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            # 任务执行失败
            response = {
                'state': task.state,
                'status': str(task.info)
            }
        
        return response
    except Exception as e:
        logger.error(f"Failed to get task status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
