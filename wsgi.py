import os
from dotenv import load_dotenv
from app import create_app
from app.utils.celery_handler import register_celery, celery

# 切换工作目录到当前文件夹
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# 启动celery是必须要读取环境变量
load_dotenv(verbose=True)
load_dotenv(dotenv_path='./.flaskenv', verbose=True)
wsgi_app = create_app(os.getenv('FLASK_ENV', 'development'))

celery = register_celery(wsgi_app, celery)

# 加上if判断可以保证在生产环境下不会启动flask自带的服务器
if __name__ == '__main__':
    print(wsgi_app.config['SQLALCHEMY_DATABASE_URI'])
    wsgi_app.run()
