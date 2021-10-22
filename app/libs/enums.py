from enum import Enum


# 客户端类型
class ClientTypeEnum(Enum):
    # 桌面端
    # 网页端
    # 用户名
    USER_NAME = 100
    # 邮箱
    USER_EMAIL = 101
    # 用户名+邮箱
    NAME_EMAIL = 102
    # 手机号
    USER_PHONE = 103

    # 第三方，包括OAuth和OpenID
    # 微信用户
    USER_WX = 200
    # 微信公众号
    # 微信小程序
    # QQ端
    # 微博
    # Github
    # Google
    # Microsoft
    # Facebook
