# -*- coding:utf-8 -*-
from . import db
from .base import Base

group_permission = db.Table('group_permission', db.Column('group_id', db.Integer, db.ForeignKey('group.id'),primary_key=True),
                             db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'),primary_key=True))


# 定义权限，与用户组多对多关系，与资源【多】对一关系
class Permission(Base):
    '''
    二进制按位授权
    1    1    1    1
    删   改   增    查
    '''
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(80))
    action = db.Column(db.Integer)
    remark = db.Column(db.String(80))
    groups = db.relationship('Group', secondary=group_permission, back_populates='permissions')
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))

# 定义资源，与权限【一】对多关系
class Resources(Base):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    resource_name = db.Column(db.String(80))
    resource_type = db.Column(db.Enum("url","element","data"),default="url")
    resource_code = db.Column(db.JSON)
    remark = db.Column(db.String(80))
    permissions = db.relationship("Permission", backref="resource", cascade="delete, delete-orphan", single_parent=True)
    __table_args__ = (db.UniqueConstraint('app_id', 'resource_name', name='_customer_uc_1'), )

class Application(Base):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(200))
    groups = db.relationship("Group",backref="application", cascade="delete, delete-orphan", single_parent=True)
    resources = db.relationship("Resources",backref="application", cascade="delete, delete-orphan", single_parent=True)
    permissions = db.relationship("Permission",backref="application", cascade="delete, delete-orphan", single_parent=True)
    resource_menu = db.relationship("ResourceMenu",backref="application", cascade="delete, delete-orphan", single_parent=True)
    perm_menu = db.relationship("PermissionMenu",backref="application", cascade="delete, delete-orphan", single_parent=True)


class ResourceMenu(Base):
    __tablename__ = 'res_menu'
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'), unique=True)
    r_menu_data = db.Column(db.JSON)
    description = db.Column(db.String(200))
    app_name = db.relationship('Application', backref='app_resource')

class PermissionMenu(Base):
    __tablename__ = 'perm_menu'
    id = db.Column(db.Integer, primary_key=True)
    p_menu_name = db.Column(db.String(80))
    checked_keys = db.Column(db.JSON)
    description = db.Column(db.String(200))
    app_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    res_menu_id = db.Column(db.Integer, db.ForeignKey('res_menu.id'))
    groups = db.relationship("Group", backref="perm_menu")
    app_name = db.relationship("Application", backref="application",single_parent=True)
    r_menu_name = db.relationship("ResourceMenu", backref="resourcemenu",single_parent=True)
    __table_args__ = (db.UniqueConstraint('app_id', 'p_menu_name', name='_customer_uc_2'),)