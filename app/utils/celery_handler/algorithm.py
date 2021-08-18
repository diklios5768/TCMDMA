# -*- encoding: utf-8 -*-
"""
@File Name      :   algorithm.py    
@Create Time    :   2021/7/28 16:01
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
from app.utils.algorithm_handler import new_analysis


@celery.task
def new_analysis_sync(**kwargs):
    new_analysis(**kwargs)
