# -*- encoding: utf-8 -*-
"""
@File Name      :   hashids.py    
@Create Time    :   2021/12/4 18:46
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
from flask import current_app
from hashids import Hashids

# hashids
hashids = Hashids(alphabet=current_app.config['HASHIDS_ALPHABET'])
