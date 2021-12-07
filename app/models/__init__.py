from flask_admin import Admin
from flask_admin.contrib import rediscli
from flask_migrate import Migrate
from flask_redis import FlaskRedis

from app.models.extension.query import Query
from app.models.extension.sqlalchemy import SQLAlchemy

# 创建数据库操作变量
db = SQLAlchemy(
    query_class=Query,
    # 是否显示SQL查询语句
    # engine_options={'echo': True}
)

# 数据库迁移
migrate = Migrate()

# 加上decode_responses=True使得取出来的str不会变成bytes类型
redis = FlaskRedis(decode_responses=True)

# 后台管理
diklios_admin = Admin(name='diklios', url='admin/diklios', endpoint='diklios_admin', template_mode='bootstrap4')
diklios_admin.add_view(rediscli.RedisCli(redis))
