from app.utils.celery_handler import celery
from app.utils.mail_handler.base import text_mail, html_mail, files_mail


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

