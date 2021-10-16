# -*- encoding: utf-8 -*-
"""
@File Name      :   encrypt.py    
@Create Time    :   2021/10/14 21:15
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

from cryptography.fernet import Fernet


def encrypt_by_cryptography(raw_str, secret_key):
    f = Fernet(secret_key)
    return f.encrypt(raw_str.encode(encoding='utf8'))


def decrypt_by_cryptography(encrypt_str, secret_key):
    f = Fernet(secret_key)
    return f.decrypt(encrypt_str).decode(encoding='utf8')
