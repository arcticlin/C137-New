# coding=utf-8
"""
File: celery_watcher.py
Author: bot
Created: 2023/9/22
Description:
"""

import subprocess, os
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 设置要监视的Celery任务模块文件
task_module_file = os.path.join(os.path.dirname(__file__), "app", "router", "jobs", "jobs.py")


def restart_worker():
    print("Restarting Celery Worker...")
    subprocess.run(["celery", "-A", "app.router.jobs.jobs", "worker", "--loglevel=INFO"])


class CeleryTaskFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(task_module_file):
            restart_worker()


if __name__ == "__main__":
    worker_thread = threading.Thread(target=restart_worker)
    worker_thread.start()
    event_handler = CeleryTaskFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
