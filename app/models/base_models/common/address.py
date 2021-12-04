from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref
from app.models.base_models.base import Base
from app.models import db


# 大洲
class Continent(Base):
    code = Column(String(10))
    name = Column(String(255))
    chinese_name = Column(String(100))
    country = relationship('Country', backref=backref('continent'))


# 国家
class Country(Base):
    continent_id = Column(Integer, ForeignKey('continent.id'), nullable=False)
    code = Column(String(10))
    name = Column(String(255))
    chinese_name = Column(String(100))
    state_or_province = relationship('StateOrProvince', backref=backref('country'))


# 国外用州，中国用省
class StateOrProvince(Base):
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
    code = Column(String(10))
    name = Column(String(255))
    chinese_name = Column(String(100))
    city = relationship('City', backref=backref('state_or_province'))

    def __init__(self, data):
        super().__init__(data.get('remarks', ''))
        self.country_id = data.get('country_id')
        self.code = data.get('code')
        self.name = data.get('name')
        self.chinese_name = data.get('chinese_name')


# 城市
class City(Base):
    state_id = Column(Integer, ForeignKey('state_or_province.id'), nullable=False)
    code = Column(String(10))
    name = Column(String(255))
    chinese_name = Column(String(100))
    area = relationship('Area', backref=backref('city'))


# 区
class Area(Base):
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    code = Column(String(10))
    name = Column(String(255))
    chinese_name = Column(String(100))
    street = relationship('Street', backref=backref('area'))


# 街道
class Street(Base):
    area_id = Column(Integer, ForeignKey('area.id'))
    name = Column(String(255))
    chinese_name = Column(String(100))


# 门牌号
class HouseNumber(Base):
    street_id = Column(Integer, ForeignKey('street.id'))
    name = Column(String(255))
    chinese_name = Column(String(100))


# 初始化中国的省份
def init_province():
    province_data = [{}]
    for i in province_data:
        data = {'country_id': 1,
                'code': i.get('code'),
                'name': i.get('name'),
                'chinese_name': i.get('chinese_name')}
        province = StateOrProvince(data)
        db.session.add(province)
    db.session.commit()
