from celery import Celery,platforms

app = Celery('tasks')
app.config_from_object('config')    #以config.py作为配置文件导入参数
platforms.C_FORCE_ROOT = True

@app.task
def add(x,y):
    return x + y