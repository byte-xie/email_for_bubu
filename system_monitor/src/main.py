#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统资源监控工具主入口
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from cli.commands import create_parser, handle_system_monitor, handle_process_monitor
from core.monitor import SystemMonitor
from config.logging_config import setup_logging, get_logger

# 设置日志配置
logger = setup_logging()


def main():
    logger.info("系统资源监控工具启动")
    logger.info("版本: 1.0.0")
    logger.info("平台: Windows")
    
    # 如果没有参数，显示系统监控
    if len(sys.argv) == 1:
        logger.info("未提供参数，使用默认系统监控模式，监控时长10秒")
        monitor = SystemMonitor()
        monitor.monitor_system(10)  # 默认监控10秒
        logger.info("默认系统监控完成")
        return
    
    # 解析命令行参数
    parser = create_parser()
    args = parser.parse_args()
    
    # 记录参数信息
    logger.info(f"接收到命令行参数: {vars(args)}")
    
    # 根据参数调用相应功能
    if args.pid or args.process_name:
        logger.info("使用进程监控模式")
        handle_process_monitor(args)
    else:
        logger.info("使用系统监控模式")
        handle_system_monitor(args)
    
    logger.info("程序执行完成")


if __name__ == "__main__":
    main()