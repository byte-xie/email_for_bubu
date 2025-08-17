#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
命令行接口模块
处理命令行参数和用户命令
"""

import argparse
import sys
import os
import logging

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.monitor import SystemMonitor
from core.process_tracker import ProcessTracker

# 获取日志记录器
logger = logging.getLogger(__name__)


def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(description='系统资源监控工具')
    parser.add_argument('--duration', type=int, default=10, help='监控持续时间（秒）')
    parser.add_argument('--pid', type=int, help='要监控的进程PID')
    parser.add_argument('--process-name', type=str, help='要监控的进程名称')
    return parser


def handle_system_monitor(args):
    """处理系统监控命令"""
    logger.info(f"开始执行系统监控，监控时长: {args.duration} 秒")
    monitor = SystemMonitor()
    monitor.monitor_system(args.duration)
    logger.info("系统监控执行完成")


def handle_process_monitor(args):
    """处理进程监控命令"""
    logger.info(f"开始执行进程监控，PID: {args.pid}, 进程名: {args.process_name}")
    tracker = ProcessTracker()
    
    if args.pid:
        process = tracker.get_process_by_pid(args.pid)
        if process:
            resources = tracker.get_process_resources(process)
            if resources:
                logger.info(f"进程 {resources['name']} (PID: {resources['pid']}) 的资源使用情况: CPU {resources['cpu_percent']}%, 内存 {resources['memory_rss']} 字节")
                print(f"进程 {resources['name']} (PID: {resources['pid']}) 的资源使用情况:")
                print(f"  CPU使用率: {resources['cpu_percent']}%")
                print(f"  内存使用: {resources['memory_rss']} 字节")
        else:
            logger.warning(f"未找到PID为 {args.pid} 的进程")
            print(f"未找到PID为 {args.pid} 的进程")
    elif args.process_name:
        processes = tracker.get_process_by_name(args.process_name)
        if processes:
            logger.info(f"找到 {len(processes)} 个名为 '{args.process_name}' 的进程")
            print(f"找到 {len(processes)} 个名为 '{args.process_name}' 的进程:")
            for process in processes:
                resources = tracker.get_process_resources(process)
                if resources:
                    logger.info(f"  PID {resources['pid']}: CPU {resources['cpu_percent']}%, 内存 {resources['memory_rss']} 字节")
                    print(f"  PID {resources['pid']}: CPU {resources['cpu_percent']}%, 内存 {resources['memory_rss']} 字节")
        else:
            logger.warning(f"未找到名为 '{args.process_name}' 的进程")
            print(f"未找到名为 '{args.process_name}' 的进程")
    logger.info("进程监控执行完成")