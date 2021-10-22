from app.utils.celery_handler import celery
from app.utils.mail_handler.base import text_mail, html_mail, files_mail
from app.utils.mail_handler.login_register import send_register_confirm_email, send_verification_code_mail


@celery.task(shared=False)
def send_text_mail_sync(subject: str = None, to: str = None, body: str = None):
    text_mail(subject, to, body)
    return True


@celery.task(shared=False)
def send_html_mail_sync(subject: str = None, to: str = None, body: str = None, html: str = None):
    html_mail(subject, to, body, html)
    return True


@celery.task(shared=False)
def send_files_mail_sync(subject: str = None, to: str = None, body: str = None, html: str = None, files: list = None):
    files_mail(subject, to, body, html, files)
    return True


@celery.task(shared=False)
def send_register_confirm_email_sync(verification_code, to=None):
    send_register_confirm_email(verification_code, to)
    return True


@celery.task(shared=False)
def send_verification_code_mail_sync(verification_code, to=None):
    send_verification_code_mail(verification_code, to)
    return True
