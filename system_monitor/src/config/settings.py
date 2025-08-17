#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理模块
管理系统的配置设置
"""

import os


class Settings:
    """系统配置类"""
    
    def __init__(self):
        """初始化配置"""
        # 默认配置
        self.default_monitoring_duration = 10
        self.default_sampling_interval = 1
        
        # 从环境变量读取配置（如果存在）
        self.monitoring_duration = int(os.getenv('MONITOR_DURATION', self.default_monitoring_duration))
        self.sampling_interval = float(os.getenv('SAMPLING_INTERVAL', self.default_sampling_interval))
    
    def get_monitoring_duration(self):
        """获取监控持续时间"""
        return self.monitoring_duration
    
    def get_sampling_interval(self):
        """获取采样间隔"""
        return self.sampling_interval