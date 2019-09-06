from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User,Group
from .role import Role
from .pms import Permission, Resources, group_permission, Application, ResourceMenu, PermissionMenu
