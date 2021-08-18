from flask import jsonify
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def csrf_error(reason):
    return
