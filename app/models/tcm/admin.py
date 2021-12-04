# -*- encoding: utf-8 -*-
"""
@File Name      :   admin.py    
@Create Time    :   2021/12/4 15:26
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

from flask_admin import Admin

tcm_admin = Admin(name='tcm', url='admin/tcm', endpoint='tcm_admin', template_mode='bootstrap4')
