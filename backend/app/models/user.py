# -*- coding:utf-8 -*-
from . import db
from .base import Base
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from passlib.apps import custom_app_context
from flask import current_app
from datetime import datetime
from .pms import group_permission

user_group = db.Table('user_group', db.Column('group_id', db.Integer, db.ForeignKey('group.id'),primary_key=True),
                             db.Column('user_id', db.Integer, db.ForeignKey('users.id'),primary_key=True))

# 定义用户组，与用户是多对多关系，与权限多对多关系
class Group(Base):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(80), unique=True)
    remark = db.Column(db.String(80))
    permissions = db.relationship('Permission',lazy='dynamic', secondary=group_permission, back_populates='groups')
    users = db.relationship('User',lazy='dynamic', secondary=user_group, back_populates='groups')
    app_id = db.Column(db.Integer, db.ForeignKey('application.id', ondelete='CASCADE'))
    perm_menu_id = db.Column(db.Integer, db.ForeignKey('perm_menu.id'))
    app_name = db.relationship('Application', backref='app_groups')

# 定义用户，与用户组是多对多关系
class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True) # 工号
    username = db.Column(db.String(80), unique=True)
    password = db.Column('password',db.String(200))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) # jobTitle
    groups = db.relationship('Group', secondary=user_group, back_populates='users')
    create_time = db.Column(db.DateTime, default=datetime.now)


    def __init__(self,username,password=None,role=None,code=None):
        self.code = code
        self.role = role
        self.username = username
        if password == None:
            password = "123456"
        self.hash_password(password)
    # 密码加密
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    # 密码解析
    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    # 获取token，有效时间10min
    def generate_auth_token(self, expiration=600000):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired as e:
            raise e  # valid token, but expired
        except BadSignature as e:
            raise e  # invalid token
        except Exception as e:
            raise e
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % self.username