from sqlalchemy import Column, String, SmallInteger, Enum, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import Base


# 使用flask-login的用户基类
class BaseUser(Base):
    __abstract__ = True
    # 用户名
    username = Column(String(100), nullable=True, index=True, unique=True)
    _password = Column('password', String(255), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    # phone_code_id = Column(ForeignKey('international_telephone_country_code.id'), nullable=True)
    phone = Column(String(12), unique=True, nullable=True)
    # 名
    first_name = Column(String(255), nullable=True,default='')
    # 姓
    last_name = Column(String(255), nullable=True,default='')
    # 别名
    nickname = Column(String(24), nullable=True,default='')
    gender = Column(Enum('male', 'female', '男', '女'), default='male', nullable=True)
    age = Column(SmallInteger, nullable=True)
    # 通过认证
    confirmed = Column(Boolean, default=False)
    # 账号是否还能（在）使用，没有被停用
    active = Column(Boolean, default=True)

    def __init__(self):
        super(BaseUser, self).__init__()
        self.set_password('default password')

    # _password属性改为只读，要设置只能通过set_password()函数
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def set_password(self, password):
        self._password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)


class BaseRole(Base):
    __abstract__ = True
    name = Column(String(50), unique=True)
    description = Column(String(255), default='')
