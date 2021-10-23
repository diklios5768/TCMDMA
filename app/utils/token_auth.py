from collections import namedtuple

from flask import request, current_app, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired

from app.libs.error_exception import TokenExpired, TokenInvalid, TokenDisabled, Forbidden
from app.libs.scope import is_in_scope
from app.viewModels.common.token import is_banned_token

User = namedtuple('User', ['uid', 'client_type', 'scopes'])
auth = HTTPBasicAuth()


# headers中Authorization:basic base64(account:password)
# 打上@auth.login_required的函数会先进入到这里
@auth.verify_password
def verify_password(account, password):
    # 此处account就是token
    # print(account)
    user_info = verify_auth_token(account)
    if not user_info:
        return False
    else:
        g.user_info = user_info
        return True


# 另一种使用新增的HTTPTokenAuth的写法
auth_token = HTTPTokenAuth(scheme='JWT')


# headers中Authorization:Bearer [BEARER_TOKEN]
@auth_token.verify_token
def verify_token(token):
    # print(token)
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user_info = user_info
        return True


# 生成token
def generate_auth_token(uid, client_type, scopes=None, expiration=7200):
    """
    uid:用户id
    ac_type:客户端类型
    scope:权限作用域
    expiration:过期时间（秒）
    """
    s = TimedJSONWebSignatureSerializer(secret_key=current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'client_type': client_type,
        'scopes': scopes
    })


# 验证token和权限
def verify_auth_token(token):
    s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    # token不合法
    except BadSignature:
        raise TokenInvalid()
    # token过期
    except SignatureExpired:
        raise TokenExpired()
    if is_banned_token(token):
        raise TokenDisabled()
    uid = data['uid']
    client_type = data['client_type']
    scopes = data['scopes']
    # 通过request拿到视图函数
    allow = is_in_scope(scopes, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, client_type, scopes)


# 获得token的信息
def get_token_info(token):
    s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token, return_header=True)
    except SignatureExpired:
        raise TokenExpired()
    except BadSignature:
        raise TokenInvalid()

    information = {
        'scopes': data[0]['scopes'],
        # 两者一起可以用于考虑是否新申请一个令牌
        # 创建时间
        'create_at': data[1]['iat'],
        # 过期时间
        'expire_in': data[1]['exp'],
        'uid': data[0]['uid'],
        'client_type': data[0]['client_type']
    }
    return information
