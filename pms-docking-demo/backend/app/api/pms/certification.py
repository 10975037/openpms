from flask_restplus import Resource
from app.api import ns
from flask import request,current_app
import requests
import json
from app.marshalling import gma


@ns.route('/pms/login/', endpoint='pms_login', methods=['POST'])
class Login(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            print("json_data",json_data)
            username = json_data['username']
            password = json_data['password']
            url = current_app.config['LOGIN_API']
            r = requests.post(url, headers={'Content-Type': 'application/json'} ,data=json.dumps({'username':username,'password':password}))
            data = r.json().get('data')
            if data['token'] is None:
                code = 50008
            else:
                code = 20000

            res = {
                'code': code,
                'data': {
                    "token": data['token']
                }
            }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'Unable create connection to PMS. Please drop email to yw@sunmi.com'
            }
        return gma.dump(res)


@ns.route('/pms/user_privilege/', endpoint='user_privilege', methods=['POST'])
class getPrivilege(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            token = json_data['token']
            url = current_app.config['PRIVILEGE_API']
            data = {
                'token': token,
                'app_id': current_app.config['APP_ID']
            }
            r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
            rr = r.json().get('data')
            res = {
                'code': 20000,
                'data': rr
            }
        except Exception as e:
            res = {
                'code': 50000,
                'message': 'Unable create connection to PMS. Please drop email to yw@sunmi.com'
            }
        return gma.dump(res)


@ns.route('/pms/logout/', endpoint='pms_logout', methods=['POST'])
class Logout(Resource):
    def post(self):
        try:
            url = current_app.config['LOGOUT_API']
            r = requests.post(url)
            rr = r.json().get('data')
            res = {
                'code': 20000,
                'data': rr
            }
        except Exception as e:
            res = {
                'code': 50000,
                'message': 'Unable create connection to PMS. Please drop email to yw@sunmi.com'
            }
        return gma.dump(res)
