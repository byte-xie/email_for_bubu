#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统资源监控核心模块
提供CPU和内存使用率的监控功能
"""

import psutil
import time
import logging


class SystemMonitor:
    """系统资源监控类"""
    
    def __init__(self):
        """初始化监控器"""
        self.logger = logging.getLogger(__name__)
    
    def get_cpu_usage(self):
        """获取CPU使用率"""
        return psutil.cpu_percent(interval=1)
    
    def get_memory_usage(self):
        """获取内存使用情况"""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
            'free': memory.free
        }
    
    def monitor_system(self, duration=10):
        """监控系统资源一段时间"""
        self.logger.info(f"开始监控系统资源 {duration} 秒")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            cpu_usage = self.get_cpu_usage()
            memory_usage = self.get_memory_usage()
            
            self.logger.info(f"CPU使用率: {cpu_usage}%")
            self.logger.info(f"内存使用率: {memory_usage['percent']}%")
            
            time.sleep(1)
        
        self.logger.info("系统资源监控完成")