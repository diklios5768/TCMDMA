# -*- encoding: utf-8 -*-
"""
@File Name      :   waitress_server.py    
@Create Time    :   2021/8/19 21:42
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

from waitress import serve
from wsgi import wsgi_app

if __name__ == '__main__':
    serve(wsgi_app, listen='*:8080')
