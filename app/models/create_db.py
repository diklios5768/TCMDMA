from app.models import db


# create_all() 和 drop_all() 方法默认作用于所有声明的绑定(bind)
# 生成数据库
def init_db(bind=None):
    if bind is None:
        db.create_all()
    else:
        db.create_all(bind=bind)


# 删除数据库
def drop_db(bind=None):
    if bind is None:
        db.drop_all()
    else:
        db.drop_all(bind=bind)


# 重新生成数据库
def recreate_db(bind=None):
    if bind is None:
        db.drop_all()
        db.create_all()
    else:
        db.drop_all(bind=bind)
        db.create_all(bind=bind)
