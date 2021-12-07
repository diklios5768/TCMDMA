from sqlalchemy import Column, String, SmallInteger, ForeignKey, delete

from app.models.base_models.base import Base


class InternationalTelephoneCountryCode(Base):
    country_code = Column(SmallInteger, index=True, nullable=False, unique=True)
    country_name = Column(String(100), nullable=False, unique=True)
    country_chinese_ame = Column(String(50), nullable=False, unique=True)


class InternationalTelephoneAreaCode(Base):
    area_code = Column(SmallInteger, index=True, nullable=False, unique=True)
    area_name = Column(String(100), nullable=False, unique=True)
    area_chinese_name = Column(String(50), nullable=False, unique=True)


class Phone(Base):
    country_code_id = Column(SmallInteger, ForeignKey('international_telephone_country_code.id'), nullable=False)
    area_code_id = Column(SmallInteger, ForeignKey('international_telephone_area_code.id'), nullable=False)
    phone_code = Column(String(20), default='', nullable=False)
