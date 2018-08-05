from __future__ import absolute_import          #如果没有这一行，下一行可能会出错          
from celery.schedules import crontab
from datetime import timedelta

BROKER_URL = 'redis://localhost:6379'

# Crontab定时任务的设置方式
# CELERYBEAT_SCHEDULE = {
#     'every-minute': {
#         'task': 'tasks.add',
#         'schedule': crontab(minute='*/1'),       #crontab的参数设置见后面
#         'args': (1,2),
#     },
# }

# Periodic task的设置方式
CELERYBEAT_SCHEDULE = {
    'add-every-2-seconds': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=2),
        'args': (16, 10),
    },
}

CELERY_TIMEZONE = 'UTC'  #时区设置，也可以为'Europe/London'