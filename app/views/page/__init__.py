# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2021/7/15 15:31
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

from flask import Blueprint, render_template

page_bp = Blueprint('page', __name__)


@page_bp.get('/', defaults={'path': ''})
@page_bp.get('/<path:path>')
def index(path):
    return render_template('sun/index.html')