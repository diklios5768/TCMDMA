from flask_migrate import Migrate
from flask_redis import FlaskRedis
# from flask_whooshee import Whooshee

from app.models.refactor.query import Query
from app.models.refactor.sqlalchemy import SQLAlchemy

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
# 全文搜索
# whooshee = Whooshee()
