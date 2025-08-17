#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
核心工具函数模块
提供系统资源监控工具的核心工具函数
"""


def format_bytes(bytes_value):
    """将字节数格式化为人类可读的格式"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_duration(seconds):
    """将秒数格式化为人类可读的时长"""
    if seconds < 60:
        return f"{seconds:.2f} 秒"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} 分钟"
    else:
        hours = seconds / 3600
        return f"{hours:.2f} 小时"