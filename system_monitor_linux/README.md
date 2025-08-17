# 系统资源监控工具

一个用于监控Linux系统资源使用情况的Python工具。

## 功能特性

- 实时监控CPU使用率
- 实时监控内存使用情况
- 进程资源使用情况跟踪
- 命令行界面支持
- 详细的日志记录功能

## 安装依赖

（可选但推荐）为项目创建独立的虚拟环境：
```bash
python3 -m venv system_monitor_env
# source system_monitor_env/bin/activate  # Linux/Mac
# system_monitor_env\Scripts\activate  # Windows
```

安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 查看帮助信息

```bash
python src/main.py --help
```

### 系统监控

默认监控10秒:
```bash
python src/main.py
```

指定监控时长:
```bash
python src/main.py --duration 30
```

### 进程监控

通过PID监控特定进程:
```bash
python src/main.py --pid 1234
```

通过进程名称监控特定进程:
```bash
python src/main.py --process-name chrome.exe
```

### 使用启动脚本

在Linux系统上，您也可以使用提供的shell脚本:
```bash
./run_monitor.sh --duration 30
```

### 日志文件

程序运行时会自动生成日志文件，日志文件位于项目根目录下的`logs`文件夹中，文件名格式为`system_monitor_YYYYMMDD.log`。

## 项目结构

```
system_monitor/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── monitor.py
│   │   ├── process_tracker.py
│   │   └── utils.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_monitor.py
│   ├── test_process_tracker.py
│   └── test_utils.py
├── docs/
├── requirements.txt
└── README.md
```

## 运行测试

```bash
python -m unittest discover tests
```