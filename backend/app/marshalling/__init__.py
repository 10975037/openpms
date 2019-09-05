from flask_marshmallow import Marshmallow
ma = Marshmallow()
from .general import gma
from .role import role_schema,roles_schema
from .user import user_schema,users_schema
from .pms import resource_schema, permission_schema, app_schema, group_schema, groups_schema, resource_menu_schema, permission_menu_schema
