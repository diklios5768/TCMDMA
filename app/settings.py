import datetime
import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# 手动载入环境变量
dotenv_path = os.path.join(basedir, '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path, verbose=True)
flask_dotenv_path = os.path.join(basedir, '../.flaskenv')
if os.path.exists(flask_dotenv_path):
    load_dotenv(dotenv_path=flask_dotenv_path, verbose=True)


# 基础环境
class BaseConfig(object):
    # Generate a nice key using secrets.token_urlsafe()
    # 使用secrets.token_urlsafe()生成一个漂亮的密钥
    SECRET_KEY = os.getenv('SECRET_KEY')
    # 需要使用cryptography.fernet。Fernet.generate_key()生成
    CRYPTOGRAPHY_SECRET_KEY = os.getenv('CRYPTOGRAPHY_SECRET_KEY')
    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # Bcrypt被设置为默认的SECURITY_PASSWORD_HASH，这需要一个salt
    # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
    # 使用secrets.SystemRandom().getrandbits(128)生成一个好的盐
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    # 配置此项会决定是否追踪对象修改，设置为False会关闭Flask-SQLAlchemy的事件通知系统，通常原来关闭警告信息
    # 如果设置成True(默认情况)，Flask - SQLAlchemy将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    # flask-sqlalchemy在2.1之后有所变化，需要一个默认值，否则报错：http://www.pythondoc.com/flask-sqlalchemy/signals.html?highlight=sqlalchemy_track_modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 从Flask - SQLAlchemy2.4.0开始，可以很容易地将选项直接传递给底层引擎。
    # 此选项确保池中的DB连接仍然有效。这对整个应用程序很重要，因为许多DBaaS选项会自动关闭空闲连接。
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
    # 是否启用HASHIDS
    HASHIDS = os.getenv('HASHIDS', False)
    # 设置默认HASHIDS ALPHABET
    HASHIDS_ALPHABET = os.getenv('HASHIDS_ALPHABET', 'diklios_skywalker_hash_password')
    # redis数据库地址
    REDIS_URL = os.getenv('REDIS_URL', 'redis://@localhost:6379/0')
    # 后台主题设置
    FLASK_ADMIN_SWATCH = os.getenv('FLASK_ADMIN_SWATCH', 'cerulean')
    # 邮件设置部分
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT', 465)
    MAIL_USE_SSL = True
    # 使用TLS的时候端口默认587
    # MAIL_USE_TLS=True
    # MAIL_PORT=os.getenv('MAIL_PORT', 587)
    # 邮箱的用户名和密码
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # 默认发件人，发送邮件不设置的时候就用这个
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    # 管理员的邮箱
    ADMIN_MAIL = os.getenv('ADMIN_MAIL', MAIL_USERNAME)
    # 用户设置
    # 登录设置
    # 设置TOKEN过期时间
    REFRESH_TOKEN_EXPIRATION = os.getenv(
        'REFRESH_TOKEN_EXPIRATION', 3600 * 24 * 7)
    ACCESS_TOKEN_EXPIRATION = os.getenv('ACCESS_TOKEN_EXPIRATION', 3600 * 2)
    # 设置登录用户默认cookies过期时间为31天，原来为365天
    REMEMBER_COOKIE_EXPIRATION = datetime.timedelta(
        days=os.getenv('REMEMBER_COOKIE_EXPIRATION', 31))
    # 验证码默认有效期10分钟
    CAPTCHA_EXPIRATION = os.getenv('CAPTCHA_EXPIRATION', 60 * 10)
    # Cookie默认只能通过http设置
    SESSION_COOKIE_HTTPONLY = bool(os.getenv('SESSION_COOKIE_HTTPONLY', True))
    # hashids的盐，如果环境变量中没设置，默认使用secret_key
    HASHIDS_SALT = os.getenv('HASHIDS_SALT', SECRET_KEY)
    # 用户文件夹设置
    USER_DIR = os.path.join(basedir, 'users')
    USER_DATA_DIR = os.path.join(basedir, 'users', 'data')
    USER_UPLOAD_DIR = os.path.join(basedir, 'users', 'upload')
    # 限制API访问
    # 限制数据存储在redis中
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', REDIS_URL)
    # 缓存
    # 缓存过期时间
    CACHE_DEFAULT_TIMEOUT = os.getenv('CACHE_DEFAULT_TIMEOUT')
    # 缓存的redis存储位置
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', REDIS_URL)


# 开发环境
class DevelopmentConfig(BaseConfig):
    # 配置数据库，如果获取不到DATABASE_URL环境变量就默认使用sqlite3，这里暂时使用sqlite开发
    # 请注意！！！Windows下的sqlite后面是三个斜杠，但是在Linux或者MacOS下是4个斜杠
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'sqlite:///' +
        os.path.join(basedir, '../tests/model/dev.db'))


# 测试环境
class TestingConfig(BaseConfig):
    Testing = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# 生产环境
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # 如果密码中含有特殊字符需要使用URL编码
    # from urllib import parse
    # SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:'+parse.quote_plus('password')+'@localhost:3306/database_name'
    SQLALCHEMY_BINDS = {
        'tcm_dma': os.getenv('SQLALCHEMY_DATABASE_URI'),
    }


# 导出环境设置
config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
