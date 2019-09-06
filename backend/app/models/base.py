from . import db


class Base(db.Model):
    __abstract__ = True
    #create_time = db.Column(db.DateTime, default=datetime.now)
