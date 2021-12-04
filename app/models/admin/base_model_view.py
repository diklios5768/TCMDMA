# -*- encoding: utf-8 -*-
"""
@File Name      :   modelview.py    
@Create Time    :   2021/12/4 10:01
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

from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView

from wtforms import TextAreaField
from wtforms.widgets import TextArea


class BaseModelView(ModelView):
    def is_accessible(self):
        if request.host=='127.0.0.1':
            return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.index', next=request.url))

    # disable model deletion
    can_delete = False
    # the number of entries to display on the list view
    page_size = 50


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class MessageAdmin(BaseModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'body': CKTextAreaField
    }
