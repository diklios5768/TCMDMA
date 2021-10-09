from flask_redis import FlaskRedis
from flask_migrate import Migrate
from app.models.refactor.query import Query
from app.models.refactor.sqlalchemy import SQLAlchemy

# 创建数据库操作变量
db = SQLAlchemy(query_class=Query)

# 数据库迁移
migrate = Migrate()
redis = FlaskRedis()
