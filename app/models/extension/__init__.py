# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py    
@Create Time    :   2021/12/7 16:55
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

from faker import Faker
from flask import current_app
from flask_whooshee import Whooshee
from hashids import Hashids

# hashids
hashids = Hashids(alphabet=current_app.config['HASHIDS_ALPHABET'])

# 全文搜索
whooshee = Whooshee()

# 生成假数据
faker = Faker()
faker_zh_CN = Faker(locale='zh_CN')
faker_zh_TW = Faker(locale='zh_TW')
