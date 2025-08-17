# Workers 目录

这个目录包含了所有与工作进程相关的模块，用于处理异步任务。

## 当前包含的文件

- `celery_worker.py`: Celery工作进程的配置和启动文件

## 管理机制

1. **文件组织**: 所有与工作进程相关的文件都应该放在这个目录中。

2. **命名规范**: 工作进程文件应该以 `_worker.py` 结尾，以便于识别。

3. **扩展性**: 当需要添加新的工作进程时，应该创建新的文件而不是修改现有文件。

4. **配置**: 工作进程的配置应该尽可能地模块化，以便于维护和扩展。

5. **日志**: 所有工作进程都应该有适当的日志记录，以便于调试和监控。

## 启动工作进程

要启动特定的工作进程，请使用以下命令：

```bash
# Celery工作进程
email_env\Scripts\celery.exe -A workers.celery_worker worker --loglevel=info
```

## 运行测试

要测试Celery工作进程的功能，请运行以下命令：

```bash
# 从项目根目录运行Celery工作进程测试
email_env\Scripts\python.exe workers/test_celery_worker.py

# 或者，从workers目录运行测试
email_env\Scripts\python.exe test_celery_worker.py
```

测试脚本会验证Celery应用的配置、任务注册和执行功能。