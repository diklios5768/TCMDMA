from celery import Celery, Task
from celery.app.control import Control


def create_celery_app():
    celery_app = Celery(__name__)  # 也可以直接把配置的值写到这里
    celery_app.config_from_object('app.utils.celery_handler.config')
    return celery_app


# celery注册上下文变量
def register_celery(app, celery_app):
    """
    Add flask app context to celery.Task
    """
    # 除非flask 中做了什么改动，以他为优先，否则并不需要更新配置
    # celery.conf.update(app.config)
    TaskBase = Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


celery = create_celery_app()
celery_control = Control(app=celery)
