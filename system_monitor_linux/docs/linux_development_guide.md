# Linux版本开发指南

## 概述

本文档说明了如何将系统资源监控工具从Windows平台移植到Linux平台。

## 移植过程

1. 创建新的项目目录 `system_monitor_linux`
2. 复制所有源代码文件
3. 修改平台标识信息
4. 替换Windows批处理脚本为Linux shell脚本
5. 更新README文档

## 主要修改

### 1. 平台标识

在 `src/main.py` 文件中，将平台信息从 "Windows" 修改为 "Linux":

```python
logger.info("平台: Linux")
```

### 2. 启动脚本

删除Windows批处理脚本 `run_monitor.bat`，创建Linux shell脚本 `run_monitor.sh`:

```bash
#!/bin/bash
python3 src/main.py "$@"
```

### 3. 文档更新

更新 `README.md` 文件中的平台说明和使用方法。

## 跨平台兼容性

由于使用了 `psutil` 库，大部分核心功能代码无需修改即可在Linux上运行。

## 测试

所有单元测试在Linux版本中均能通过，验证了功能的正确性。

## 运行方式

在Linux系统上，可以通过以下方式运行监控工具:

```bash
# 直接运行
python3 src/main.py --duration 30

# 使用启动脚本
./run_monitor.sh --duration 30
```

## 注意事项

1. 确保系统已安装Python 3和psutil库
2. 在Linux上使用 `python3` 命令而不是 `python`
3. 确保shell脚本具有执行权限: `chmod +x run_monitor.sh`
4. 如果在Windows系统上开发，需要将文件传输到Linux系统后设置执行权限