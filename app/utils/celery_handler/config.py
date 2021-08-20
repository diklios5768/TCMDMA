# celery的默认设置

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/1'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
result_accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = True
