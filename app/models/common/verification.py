# -*- encoding: utf-8 -*-
"""
@File Name      :   verification.py    
@Create Time    :   2021/7/14 21:00
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

from sqlalchemy import Column, String, Integer, Boolean
from app.models.base import Base


class EmailVerification(Base):
    email = Column(String(255), nullable=False)
    # 验证码
    verification_code = Column(String(10), nullable=False)
    # 有效期
    expiration = Column(Integer, nullable=False)
    # 用途
    use = Column(String(20), nullable=False)
    # 现在是否失效（可能被使用，也可能手动过期）
    valid = Column(Boolean, default=True)


class PhoneVerification(Base):
    # phone_code=Column(String(4),nullable=False)
    phone = Column(String(12), nullable=False)
    verification_code = Column(String(10), nullable=False)
    expiration = Column(Integer, nullable=False)
    use = Column(String(20), nullable=False)
    valid = Column(Boolean, default=True)
