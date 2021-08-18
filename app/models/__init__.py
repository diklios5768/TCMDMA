from flask_redis import FlaskRedis
from flask_security import Security
from flask_migrate import Migrate
from faker import Faker

from app.models.refactor.query import Query
from app.models.refactor.sqlalchemy import SQLAlchemy

# 创建数据库操作变量
db = SQLAlchemy(query_class=Query)

security = Security()
# 数据库迁移
migrate = Migrate()
redis = FlaskRedis()
# 假数据
fake = Faker()
fake_zh_CN = Faker('zh_CN')
fake_en_US = Faker('en_US')
