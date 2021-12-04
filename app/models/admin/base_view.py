# -*- encoding: utf-8 -*-
"""
@File Name      :   admin_view.py    
@Create Time    :   2021/12/4 18:10
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

from flask_admin import BaseView as _BaseView, expose


class BaseView(_BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')
