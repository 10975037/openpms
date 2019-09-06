from . import ma
from app.models import Permission, Resources, Application, Group, ResourceMenu, PermissionMenu


class PermissionSchema(ma.ModelSchema):
    class Meta:
        include_fk = True
        model = Permission


class ResourceSchema(ma.ModelSchema):
    class Meta:
        model = Resources


class AppSchema(ma.ModelSchema):
    class Meta:
        model = Application


app_schema = AppSchema(many=True)
permission_schema = PermissionSchema(many=True)
resource_schema = ResourceSchema(many=True)


# 序列化组列表
class GroupSchema(ma.ModelSchema):
    app_name = ma.Nested(AppSchema, only=["app_name"])
    class Meta:
        model = Group
        # include_fk = True


group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)


class ResourceMenuSchema(ma.ModelSchema):
    app_name = ma.Nested(AppSchema, only=["app_name"])
    class Meta:
        model = ResourceMenu
        include_fk = True


class PermissionMenuSchema(ma.ModelSchema):
    app_name = ma.Nested(AppSchema, only=["app_name"])
    class Meta:
        include_fk = True
        model = PermissionMenu


resource_menu_schema = ResourceMenuSchema(many=True)
permission_menu_schema = PermissionMenuSchema(many=True)