#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日志配置模块
配置系统的日志记录设置
"""

import logging
import os
from datetime import datetime


def setup_logging(log_dir="logs", log_level=logging.INFO):
    """设置日志配置"""
    # 创建日志目录
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 生成日志文件名
    log_filename = os.path.join(log_dir, f"system_monitor_{datetime.now().strftime('%Y%m%d')}.log")
    
    # 配置根日志记录器
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()  # 同时输出到控制台
        ]
    )
    
    return logging.getLogger(__name__)


def get_logger(name):
    """获取指定名称的日志记录器"""
    return logging.getLogger(name)