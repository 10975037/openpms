from flask_restplus import Resource
from app.api import ns
from flask import request, jsonify, current_app
from app.models import db
from app.models import Application
from app.marshalling import app_schema, gma
from app.utils import authenticate

@ns.route('/pms/application/', endpoint='application', methods=['GET', 'POST', 'PUT', 'DELETE'])
class AppApi(Resource):
    method_decorators = [authenticate]
    def get(self, *args, **kwargs):
        try:
            app_id = request.args.get('id')
            if app_id == '':
                records = Application.query.all()
            else:
                records = Application.query.filter_by(id=app_id)
            res = {
                'code': 20000,
                'data': app_schema.dump(records)
            }
        except Exception as e:
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to query APP. Please drop email to yw@sunmi.com'
            }
            current_app.logger.error(str(e))
        finally:
            db.session.close()
        return jsonify(res)

    def post(self):
        try:
            json_data = request.get_json()
            app_name = json_data['app_name']
            desc = json_data['desc']
            record = Application(app_name=app_name, description=desc)
            db.session.add(record)
            db.session.commit()
            res = {
                'code': 20000,
            }
        except Exception as e:
            current_app.logger.error(str(e))
            db.session.rollback()
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to add APP. Please drop email to admin@devopser.org'
            }
        finally:
            db.session.close()
        return jsonify(res)

    def put(self):
        try:
            json_data = request.get_json()
            app_id = json_data['app_id']
            app_name = json_data['app_name']
            desc = json_data['desc']

            record = Application.query.filter_by(id=app_id).first()
            record.app_name = app_name
            record.description = desc
            db.session.commit()
            res = { 'code': 20000 }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to update APP. Please drop email to yw@sunmi.com'
            }
        finally:
            db.session.close()
        return jsonify(res)

    def delete(self, *args, **kwargs):
        try:
            app_id = request.args.get('id')
            record = Application.query.filter_by(id=app_id).first()
            db.session.delete(record)
            db.session.commit()
            res = { 'code': 20000 }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'messgae': 'ERROR: Failed to delete APP. Please drop email to yw@sunmi.com'
            }
        finally:
            db.session.close()
        return jsonify(res)



@ns.route('/pms/apps_selector/',endpoint="apps_selector",methods=['GET'])
class AppSelector(Resource):
    # method_decorators = [authenticate]
    def get(self):
        # from flask import g
        # print(g.user.code)
        apps = Application.query.all()
        apps_selector = []
        try:
            for app in apps:
                apps_selector.append({ "label":app.app_name,"value":app.id })
            code = 20000
        except Exception as e:
            code = 50000
            apps_selector = "获取失败：%s" % str(e)
        finally:
            db.session.close()

        data = {
            'code':code,
            'data':apps_selector
        }
        return gma.dump(data)


@ns.route('/pms/app_unqiue_check/',endpoint="app_unqiue_check",methods=['GET'])
class AppWithName(Resource):
    def get(self, *args, **kwargs):
        try:
            app_name = request.args.get('app_name')
            total = Application.query.filter_by(app_name=app_name).count()
            if total is not 0:
                result = 1
            else:
                result = 0

            res = {
                'code': 20000,
                'data': result
            }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to query App. Please drop email to yw@sunmi.com'
            }
        finally:
            db.session.close()
        return jsonify(res)

