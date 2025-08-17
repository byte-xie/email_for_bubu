# 系统资源监控工具用户手册

## 简介

系统资源监控工具是一个轻量级的Python应用程序，用于监控Windows系统的CPU和内存使用情况，以及跟踪特定进程的资源使用情况。

## 安装

1. 确保您的系统上安装了Python 3.7或更高版本
2. 克隆或下载项目代码
3. （可选但推荐）为项目创建独立的虚拟环境：
   ```bash
   python -m venv system_monitor_env
   system_monitor_env\Scripts\activate  # Windows
   # source system_monitor_env/bin/activate  # Linux/Mac
   ```
4. 安装依赖包：

```bash
pip install -r requirements.txt
```

## 基本使用

### 系统监控

要监控整个系统的资源使用情况，可以直接运行程序：

```bash
python src/main.py
```

这将默认监控系统10秒钟，并显示CPU和内存使用率。

要指定监控时长，可以使用`--duration`参数：

```bash
python src/main.py --duration 30
```

在Windows系统上，您也可以使用提供的批处理脚本:

```bash
run_monitor.bat --duration 30
```

### 进程监控

要监控特定进程的资源使用情况，可以使用`--pid`或`--process-name`参数：

通过进程ID监控：
```bash
python src/main.py --pid 1234
```

通过进程名称监控：
```bash
python src/main.py --process-name chrome.exe
```

## 命令行参数

- `--duration DURATION`: 监控持续时间（秒），默认为10秒
- `--pid PID`: 要监控的进程PID
- `--process-name PROCESS_NAME`: 要监控的进程名称
- `--help`: 显示帮助信息

## Windows批处理脚本

在Windows系统上，您也可以使用提供的`run_monitor.bat`脚本来运行程序：

```bash
run_monitor.bat --duration 30
```

## 故障排除

### ImportError: No module named 'psutil'

如果遇到此错误，请确保已安装依赖包：

```bash
pip install -r requirements.txt
```

### 找不到指定的进程

如果使用`--pid`或`--process-name`参数时提示找不到进程，请确保：
1. 进程ID或名称正确
2. 进程正在运行
3. 您有足够的权限访问该进程

## 日志功能

系统资源监控工具现在包含了详细的日志记录功能，可以帮助用户更好地了解程序运行状态和排查问题。

### 日志文件位置

程序运行时会自动生成日志文件，日志文件位于项目根目录下的`logs`文件夹中，文件名格式为`system_monitor_YYYYMMDD.log`。

### 日志级别

工具使用了标准的Python日志级别：
- INFO: 记录程序正常运行的信息
- WARNING: 记录可能的问题或异常情况
- ERROR: 记录错误事件

### 日志内容

日志文件包含以下信息：
- 程序启动和结束时间
- 命令行参数解析结果
- 监控过程中的资源使用情况
- 进程查找和监控结果
- 错误和异常信息

用户可以通过查看日志文件来了解程序的详细运行情况，特别是在出现异常时可以帮助快速定位问题。