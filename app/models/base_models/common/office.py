from sqlalchemy import Column, String
from app.models.base_models.base import Base


# 部门，包括行政部门和特殊部门
class Office(Base):
    name = Column(String(100))
    english_name = Column(String(100))
    code = Column(String(10))
