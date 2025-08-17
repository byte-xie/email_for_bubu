#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
通用辅助函数模块
提供系统资源监控工具的通用辅助函数
"""


def validate_positive_integer(value, name):
    """验证正整数值"""
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} 必须是正整数")
    return value


def validate_non_negative_float(value, name):
    """验证非负浮点数值"""
    if not isinstance(value, float) or value < 0:
        raise ValueError(f"{name} 必须是非负浮点数")
    return value