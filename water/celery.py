from __future__ import absolute_import,unicode_literals
import os
from celery import Celery,platforms

#set the default django setting module for the 'celery' program
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'water.settings')

#这里还是采redis来作MQ配置
#app = Celery('water',backend='redis',broker = "redis://localhost")
app = Celery("water",backend="redis://127.0.0.1:6379/0",broker="redis://127.0.0.1:6379/1")
# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
#app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# 允许root 用户运行celery
platforms.C_FORCE_ROOT = True

#因为考虑到celery长时间运行可能出现内存泄漏，因此添加此选项，表示每个worker执行了10个任务后就结束

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
