from flask_restplus import Resource
from app.api import ns
from flask import request,jsonify,current_app
from app.api.user import UserInfoBody
from app.marshalling import gma
from app.utils import auth


@ns.route('/pms/getPrivilege/',endpoint='get_privilege',methods=['POST'])
class GetPrivilege(Resource):
    def post(self):
        """向其他系统提供菜单/界面元素等资源"""
        json_data = request.get_json()
        token = json_data['token']
        app_id = json_data['app_id']
        (user, element_list, menurouter, group_name) = UserInfoBody(token, app_id)

        data = {
            'code': 20000,
            "data": {
                'token': token,
                'group': group_name if group_name else "No Data",
                'name': user.username,
                'avatar': None,
                'element_perms': element_list,
                'routers': menurouter
            }
        }
        current_app.logger.info('获取用户信息')
        return gma.dump(data)


@ns.route('/pms/apiPrivilege/',endpoint='api_privilege',methods=['POST'])
class ApiPrivilege(Resource):
    def post(self):
        """向其他系统提供URL资源"""
        json_data = request.get_json()
        token = json_data['token']
        app_id = json_data['app_id']
        path = json_data['path']
        method = json_data['method']
        result = auth(app_id, token, path, method)

        res = {
            'code': 20000,
            'data': result
        }
        return jsonify(res)