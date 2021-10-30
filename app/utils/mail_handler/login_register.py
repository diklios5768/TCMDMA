from flask import render_template
from flask_mail import Message
from app.utils.celery_handler import celery
from . import mail


# def send_register_token_email(token, to=None):
#     if not to:
#         return False
#     message = Message(
#         subject='Email Confirm',
#         recipients=[to],
#         body=render_template('mail/register_token.txt', token=token),
#         html=render_template('mail/register_token.html', token=token)
#     )
#     mail.send(message)

@celery.task(shared=False)
def send_register_confirm_email(register_link, to=None):
    if not to:
        return False
    message = Message(
        subject='注册验证',
        recipients=[to],
        body=render_template('mail/register.txt', register_link=register_link),
        html=render_template('mail/register.html', register_link=register_link)
    )
    mail.send(message)

# def send_reset_password_token_email(user, token, to=None):
#     message = Message(
#         subject='Reset password',
#         recipients=[to] or [user.email],
#         body=render_template('mail/reset_password_token.txt', token=token, user=user),
#         html=render_template('mail/reset_password_token.html', token=token, user=user)
#     )
#     mail.send(message)
#
#
# def send_reset_password_confirm_email(user, token, to=None):
#     message = Message(
#         subject='Reset password',
#         recipients=[to] or [user.email],
#         body=render_template('mail/reset_password.txt', token=token, user=user),
#         html=render_template('mail/reset_password.html', token=token, user=user)
#     )
#     mail.send(message)


@celery.task(shared=False)
def send_captcha_mail(captcha, to=None):
    if not to:
        return False
    message = Message(
        subject='验证码',
        recipients=[to],
        body=render_template('mail/captcha.txt', captcha=captcha),
        html=render_template('mail/captcha.html', captcha=captcha)
    )
    mail.send(message)