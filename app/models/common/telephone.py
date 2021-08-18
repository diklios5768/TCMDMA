from sqlalchemy import Column, String, SmallInteger

from app.models.base import Base


class InternationalTelephoneCountryCode(Base):
    country_code = Column(SmallInteger, index=True, nullable=False, unique=True)
    country_name = Column(String(100), nullable=False, unique=True)
    country_chinese_ame = Column(String(50), nullable=False, unique=True)


class InternationalTelephoneAreaCode(Base):
    area_code = Column(SmallInteger, index=True, nullable=False, unique=True)
    area_name = Column(String(100), nullable=False, unique=True)
    area_chinese_name = Column(String(50), nullable=False, unique=True)
