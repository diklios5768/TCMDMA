from flask import render_template
from flask_mail import Message
from . import mail


def test_register_mail(subject, to, content):
    message = Message(
        # 主题
        subject=subject or 'hello world',
        # 接受人，接收一个数组，可以是多个接收者
        recipients=to or ['1061995104@qq.com'],
        # 正文
        body=render_template('mail/base.txt', content=content),
        # 网页形式的正文
        html=render_template('mail/base.html', content=content)
    )
    mail.send(message)


def send_register_confirm_email(user, token, to=None):
    message = Message(
        subject='Email Confirm',
        recipients=to or user.email,
        body=render_template('mail/register.txt', token=token, user=user),
        html=render_template('mail/register.html', token=token, user=user)
    )
    mail.send(message)


def send_reset_password_email(user, token, to=None):
    message = Message(
        subject='Reset password',
        recipients=to or user.email,
        body=render_template('mail/reset_password.txt', token=token, user=user),
        html=render_template('mail/reset_password.html', token=token, user=user)
    )
    mail.send(message)
