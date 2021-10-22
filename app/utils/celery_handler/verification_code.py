# -*- encoding: utf-8 -*-
"""
@File Name      :   verification_code.py    
@Create Time    :   2021/10/22 19:45
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

from app.utils.celery_handler import celery

from app.utils.file_handler.text_handler.verification_code import delete_verification_code


@celery.task(shared=False)
def delete_verification_code_sync(code):
    delete_verification_code(code)
    return True
