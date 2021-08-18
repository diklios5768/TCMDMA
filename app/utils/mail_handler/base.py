# Email Service Provider，即ESP,使用QQ，163等邮箱发送
# 注意，邮件最好提供HTML和txt两种样式，以便用户查看，使用jinja2模板组织正文
from flask_mail import Message
from . import mail


# 传入文本信息的邮件
def text_mail(subject: str = None, to: str = None, body: str = None):
    message = Message(
        # 主题
        subject=subject or 'hello world',
        # 接受人，接收一个数组，可以是多个接收者
        recipients=to or ['1061995104@qq.com'],
        # 正文
        body=body or 'Test text',
    )
    mail.send(message)


# 有HTML和txt的混合邮件
def html_mail(subject: str = None, to: str = None, body: str = None, html: str = None):
    message = Message(
        # 主题
        subject=subject or 'hello world',
        # 接受人，接收一个数组，可以是多个接收者
        recipients=to or ['1061995104@qq.com'],
        # 正文
        body=body or 'Test html',
        # 网页形式的正文
        html=html or '<h1>Just Test HTML</h1>'
    )
    mail.send(message)


# 发送附件
def files_mail(subject: str = None, to: str = None, body: str = None, html: str = None, files: list = None):
    """
    files:[{
    "path":str,
    "name":str,
    "content_type":str
    },...]
    """
    message = Message(
        # 主题
        subject=subject or 'hello world',
        # 接受人，接收一个数组，可以是多个接收者
        recipients=to or ['1061995104@qq.com'],
        # 正文
        body=body or 'Test PDF',
        # 网页形式的正文
        html=html or '<h1>Just Test PDF</h1>'
    )
    if files is None:
        return False
    # 添加附件
    for file in files:
        print('mail'+file['path'])
        with open(file['path'], 'rb') as f:
            file_data = f.read()
            message.attach(filename=file['name'], disposition='attachment', content_type=file['content_type'],
                           data=file_data)
    mail.send(message)
