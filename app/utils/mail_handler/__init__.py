from flask_mail import Mail
# 可以使用sendgrid，请先去注册
# 用于发送邮件
mail = Mail()


# 异步发送邮件
def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)

