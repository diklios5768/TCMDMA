from datetime import datetime

from sqlalchemy import Column, Integer, String, SmallInteger, Float,JSON
from sqlalchemy.orm import reconstructor
from app.libs.error_exception import ParameterException
from app.models import db


# todo:给id添加加密和解密
class Base(db.Model):
    """
    基类，不会构建
    id：id
    remarks：备注
    create_time：创建时间
    modify_time：上一次修改时间
    status：状态
    """
    __abstract__ = True
    # 注意SQLite的AUTOINCREMENT只适用于INTEGER，开发的时候一点小心
    # 如果其他的需要自增，可以使用BigInteger().with_variant(Integer, "sqlite")
    id = Column(Integer, primary_key=True, nullable=False, index=True, unique=True, autoincrement=True)
    remarks = Column(String(1024), nullable=True, default='')
    json_remarks=Column(JSON,nullable=True,default={})
    # 使用datetime.utcnow()保证迁移服务器后使用的时间还是一致的
    # 时间存储的时候推荐使用时间戳，因为时间格式多种多样，而时间戳是通用的数字
    create_time = Column(Float, nullable=True, default=datetime.utcnow().timestamp())
    modify_time = Column(Float, nullable=True, default=datetime.utcnow().timestamp())
    status = Column(SmallInteger, nullable=True, default=1)
    fields = []

    # 因为SQLAlchemy-ORM是通过元类创建的（很多其他数据库的orm都是通过元类创建的），他不执行__init__()函数，所以需要打上一个reconstructor装饰器才能够执行
    # 如查询的时候创建的对象就不执行__init__()
    # 但是如果通过Class()这种形式创建还是会执行__init__()的
    # 即如果不是自己以创建对象的形式创建的对象，而是sqlalchemy自动创建的对象，不执行__init__()
    # 继承基类的模型如果需要初始化同样需要打上reconstructor装饰器
    @reconstructor
    def __init__(self):
        self.remarks = ''
        self.create_time = datetime.utcnow().timestamp()
        self.modify_time = datetime.utcnow().timestamp()
        self.status = 1
        # 注意fields必须是实例变量，基类中为空

    # 用于使用dict(orm.model)返回需要的字段
    # 获得keys之后，会调用__getitem__()函数，所以需要重写
    def __getitem__(self, item):
        return getattr(self, item)

    # 需要的字段，名称必须是keys，因为这是dict()函数默认先调用的函数
    def keys(self):
        return self.fields

    # 直接重新设置fields，可以用列表，也可以传入多个参数
    def set_fields(self, new_filed_list: list, *new_fields):
        self.fields = [*new_filed_list, *new_fields]
        return self

    # 从现在的fields中需要被移除的字段
    def hide_fields(self, *hide_keys):
        for key in hide_keys:
            if key in self.fields:
                self.fields.remove(key)
        return self

    # 再次在fields中添加字段
    def append_fields(self, *append_keys):
        for key in append_keys:
            self.fields.append(key)
        self.fields = list(set([*self.fields, *append_keys]))
        return self

    # 获得所有实例化的属性，转化为字典，尽量不使用，而是在具体的模型中定义keys函数
    # 与上面设计的dict()方法不同的是，这样返回的字段是所有不带__和_字段，只有一种，不够灵活
    def get_dict(self):
        self_dict = {}
        for key, value in self.__dict__.items():
            if not (key.startswith('__') or key.startswith('_') or key.endswith('__')):
                self_dict[key] = value
        return self_dict

    # 手动更新一下修改时间
    def touch(self):
        self.modify_time = datetime.utcnow().timestamp()

    def set_status(self, status):
        """
        1:可查询
        0:不可查询
        一个函数可以代替下面两个函数
        """
        self.status = status
        self.modify_time = datetime.utcnow().timestamp()

    def remove(self):
        self.status = 0
        self.modify_time = datetime.utcnow().timestamp()

    def recover(self):
        self.status = 1
        self.modify_time = datetime.utcnow().timestamp()

    def delete(self):
        self.status = -1
        self.modify_time = datetime.utcnow().timestamp()

    def set_remarks(self, remarks=''):
        self.remarks = remarks
        self.modify_time = datetime.utcnow().timestamp()

    def set_attrs(self, attrs_dict, **kwargs):
        """
        根据传回的参数修改属性值，但是id不能修改
        """
        attrs_dict = {**attrs_dict, **kwargs}
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != "id" and key != 'password':
                setattr(self, key, value)
            else:
                raise ParameterException()
            # 如果create_time传回来的是字符串，且本身类型是datetime则可以使用这个方法重写格式化
            # 使用时间戳之后不需要再用这个方法了
            # if key == 'create_time':
            #     setattr(self, key, datetime.strptime(value, '%a, %d %b %Y %H:%M:%S GMT'))
        self.modify_time = datetime.utcnow().timestamp()

    # 返回一个规范化的日期字符串，如果前端需要跨时区，就不需要使用这个方法
    @property
    def get_format_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    # 基类中使用外键的方法
    # 原因是每个模型必须具有唯一的orm属性.如果mixin中的相同属性直接应用于每个子类, 则它们都具有相同的属性.基本orm属性的副本很容易创建, 因为它们不引用任何其他orm属性.对于更复杂的属性,
    # 使用 @declared_attr修饰的函数可确保为每个子类创建新实例
    # 在检测期间, SQLAlchemy为每个类调用每个声明的attr, 并将结果分配给目标名称.通过这种方式, 它可以确保为每个子类唯一且正确地进行复杂映射
    # @declared_attr
    # 此处必须命名为cls,而不是self
    # def foreign_key(cls):
    # return Column(...)
