import os

from dotenv import load_dotenv

from app import create_app
from app.utils.celery_handler import register_celery, celery

# 切换工作目录到当前文件夹
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
# 手动载入环境变量
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path, verbose=True)
flask_dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(flask_dotenv_path):
    load_dotenv(dotenv_path=flask_dotenv_path, verbose=True)

# 创建flask_app
wsgi_app = create_app(os.getenv('FLASK_ENV', 'development'))
# 创建celery_app
celery = register_celery(wsgi_app, celery)

# 加上if判断可以保证在生产环境下不会启动flask自带的服务器
if __name__ == '__main__':
    # 多进程或多线程只能选择一个，不能同时开启
    # 使用ipv6运行
    # wsgi_app.run(host='::')
    wsgi_app.run(threaded=True)
