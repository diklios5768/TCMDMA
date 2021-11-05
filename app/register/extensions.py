# attention:一些不怎么需要配置的扩展在这里定义
# from flask_socketio import SocketIO
# from flask_moment import Moment
# from flask_babel import Babel
from flask_caching import Cache
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.models import db, migrate, redis
from app.utils.mail_handler import mail

# socket_io = SocketIO()
# moment = Moment()
# 后端国际化
# babel = Babel()
cors = CORS()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "100 per hour", "20 per minute"],
    # X-RateLimit写入响应头
    headers_enabled=True,
)
# 使用redis进行缓存存储
cache = Cache(config={'CACHE_TYPE': 'redis'})


# 注册插件,全部使用init_app的方法生成
def register_extensions(app):
    # 切记数据库生成的代码必须放在数据库相关配置都配置好了之后再生成,这点非常重要
    db.init_app(app)
    # 数据库迁移
    migrate.init_app(app, db)
    # 注册redis数据库
    redis.init_app(app)
    # 注册邮件配置
    mail.init_app(app)
    # 跨域
    cors.init_app(app, supports_credentials=True)
    # 设置api调用限制
    limiter.init_app(app)
    # 设置缓存
    cache.init_app(app)
