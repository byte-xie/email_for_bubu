#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
进程资源监控模块
提供对特定进程的CPU和内存使用率监控功能
"""

import psutil
import logging


class ProcessTracker:
    """进程资源监控类"""
    
    def __init__(self):
        """初始化进程监控器"""
        self.logger = logging.getLogger(__name__)
    
    def get_process_by_pid(self, pid):
        """通过PID获取进程信息"""
        try:
            process = psutil.Process(pid)
            self.logger.info(f"成功获取到PID为 {pid} 的进程信息")
            return process
        except psutil.NoSuchProcess:
            self.logger.warning(f"未找到PID为 {pid} 的进程")
            return None
        except Exception as e:
            self.logger.error(f"获取PID为 {pid} 的进程时发生错误: {e}")
            return None
    
    def get_process_by_name(self, name):
        """通过名称获取进程信息"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == name:
                    processes.append(psutil.Process(proc.info['pid']))
            self.logger.info(f"通过名称 '{name}' 找到 {len(processes)} 个进程")
            return processes
        except Exception as e:
            self.logger.error(f"通过名称 '{name}' 查找进程时发生错误: {e}")
            return processes
    
    def get_process_resources(self, process):
        """获取进程的资源使用情况"""
        try:
            cpu_percent = process.cpu_percent()
            memory_info = process.memory_info()
            
            resources = {
                'pid': process.pid,
                'name': process.name(),
                'cpu_percent': cpu_percent,
                'memory_rss': memory_info.rss,
                'memory_vms': memory_info.vms
            }
            self.logger.info(f"获取到进程 {process.pid} 的资源信息: CPU {cpu_percent}%, 内存RSS {memory_info.rss} 字节")
            return resources
        except psutil.NoSuchProcess:
            self.logger.warning(f"进程 {process.pid} 已不存在")
            return None
        except Exception as e:
            self.logger.error(f"获取进程 {process.pid} 资源信息时发生错误: {e}")
            return None