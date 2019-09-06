from functools import wraps
from flask import request,jsonify,g, current_app
from app.models import db,User
from app.utils.map_perm import mapPerm


def auth(app_id = None, t = None, path = None, method = None):
    TOKEN = t # token 目的是为了向其他对接系统提供鉴权服务
    APP_ID = app_id # app_id 目的是为了向其他对接系统提供鉴权服务
    PATH = path #  path 目的是为了向其他对接系统提供鉴权服务
    METHOD = method #  method 目的是为了向其他对接系统提供鉴权服务

    try:
        user = User.verify_auth_token(TOKEN)
        g.user = user
    except Exception as e:
        return False
    finally:
        db.session.commit()

    # APP_ID为1是PMS系统自身，user.id为1是PMS管理员
    if APP_ID is 1 and user.id is 1:
        return True

    groups = user.groups

    for group in groups:
        if group.app_id is APP_ID:
            permissions = group.permissions
            for perm in permissions:
                if perm.resource.resource_type is 'url' and perm.resource.resource_code.get("url") == PATH:
                    res = mapPerm.auth_method(METHOD,perm.action)
                    print(user.username,perm.resource.resource_name,perm.resource.resource_code,res)
                    return res
    return False


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        判断用户是否有权限访问URL
        1、获取当前请求方法和请求url
        2、根据用户获当拥有的前系统下组权限，取出resource_code
        3、校验resource_code等于请求url的资源的action是否包含请求方法
        """
        token = None
        if 'X-Token' in request.headers:
            token = request.headers['X-Token']
        acct = auth(current_app.config['APP_ID'], token, request.path, request.method)
        if acct:
            return func(*args, **kwargs)
        return jsonify({"code": 40000, "message": "无权访问"})
    return wrapper