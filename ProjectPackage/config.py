import os
class Config(object):
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置時區
    SCHEDULER_API_ENABLED = True
    SCHEDULER_API_PREFIX = '/scheduler'
    # 配置允许执行定时任务的主机名
    SCHEDULER_ALLOWED_HOSTS = ['*']
    SECRET_KEY=os.urandom(16).hex()#隨機產生16進位的亂數作為密鑰