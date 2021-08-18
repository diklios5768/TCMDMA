# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/7/14 9:53
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

from flask import Blueprint
from app.libs.error_exception import Success
from app.views.api.v1_0 import v1_0_bp
from app.utils.celery_handler.mail import send_text_mail_sync
from app.utils.mail_handler.base import text_mail

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(v1_0_bp, url_prefix='/v1_0')


@api_bp.get('/test_celery_mail')
def test_celery_mail():
    send_text_mail_sync.delay()
    return Success()


@api_bp.get('/test_mail')
def test_mail():
    text_mail()
    return Success()
