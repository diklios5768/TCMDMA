from flask_redis import FlaskRedis
from flask_migrate import Migrate
from app.models.refactor.query import Query
from app.models.refactor.sqlalchemy import SQLAlchemy

# 创建数据库操作变量
db = SQLAlchemy(query_class=Query)

# 数据库迁移
migrate = Migrate()
# 加上decode_responses=True使得取出来的str不会变成bytes类型
redis = FlaskRedis(decode_responses=True)
