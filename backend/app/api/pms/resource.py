from flask_restplus import Resource
from app.api import ns
from flask import request, jsonify, current_app
from app.models import db
from app.models import Resources, ResourceMenu
from app.marshalling import resource_schema, resource_menu_schema
import json


@ns.route('/pms/resource/', endpoint='resource', methods=['GET', 'POST', 'PUT', 'DELETE'])
class ResourceApi(Resource):
    def get(self, *args, **kwargs):
        try:
            query = request.args.get('query')
            query = json.loads(query)
            if  'id' in query:
                record = Resources.query.filter_by(id=query['id'])
                res = {
                    'code': 20000,
                    'data': resource_schema.dump(record)
                }
            else:
                if 'type' in query and 'name' in query:
                    total = Resources.query.filter(
                        Resources.app == query['appId'],
                        Resources.resource_type == query['type'],
                        Resources.resource_name.contains(query['name'])
                    ).count()

                    records = Resources.query.filter(
                        Resources.app == query['appId'],
                        Resources.resource_type == query['type'],
                        Resources.resource_name.contains(query['name'])
                    ).order_by(Resources.id).paginate(int(query['page']), int(query['limit']), error_out=False)

                    r_data = records.items

                elif 'type' in query and 'name' not in query:
                    total = Resources.query.filter(
                        Resources.app_id == query['appId'],
                        Resources.resource_type == query['type']
                    ).count()

                    records = Resources.query.filter(
                        Resources.app_id == query['appId'],
                        Resources.resource_type == query['type']
                    ).order_by(Resources.id).paginate(int(query['page']), int(query['limit']), error_out=False)

                    r_data = records.items

                elif 'type' not in query and 'name' in query:
                    total = Resources.query.filter(
                        Resources.app_id == query['appId'],
                        Resources.resource_name.contains(query['name'])
                    ).count()

                    records = Resources.query.filter(
                        Resources.app_id == query['appId'],
                        Resources.resource_name.contains(query['name'])
                    ).order_by(Resources.id).paginate(int(query['page']), int(query['limit']), error_out=False)

                    r_data = records.items

                else:
                    total = Resources.query.filter(
                        Resources.app_id == query['appId']
                    ).count()

                    records = Resources.query.filter(
                        Resources.app_id == query['appId']
                    ).order_by(Resources.id).paginate(int(query['page']), int(query['limit']), error_out=False)

                    r_data = records.items

                res = {
                    'code': 20000,
                    'total': total,
                    'data': resource_schema.dump(r_data)
                }

        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to query resource. Please drop email to yw@sunmi.com'
            }
        finally:
            db.session.close()
        return jsonify(res)

    def post(self):
        try:
            json_data = request.get_json()
            app_id = json_data['app_id']
            resource_name = json_data['resource_name']
            resource_type = json_data['resource_type']
            resource_code = json_data['resource_code']
            if resource_type != 'menu':
                resource_code = json.loads(resource_code)
            desc = json_data['desc']
            print(resource_code)
            record = Resources(app_id=app_id, resource_name=resource_name, resource_type=resource_type,
                               resource_code=resource_code, remark=desc)
            db.session.add(record)
            db.session.commit()
            res = { 'code': 20000 }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to add resource. Please drop email to yw@sunmi.com'
            }
        finally:
            db.session.close()
        return jsonify(res)

    def put(self):
        try:
            json_data = request.get_json()
            resource_id = json_data['resource_id']
            app_id = json_data['app_id']
            resource_name = json_data['resource_name']
            resource_type = json_data['resource_type']
            resource_code = json_data['resource_code']
            if resource_type != 'menu':
                resource_code = json.loads(resource_code)
            desc = json_data['desc']
            record = Resources.query.filter_by(id=resource_id).first()
            record.app_id = app_id
            record.resource_name = resource_name
            record.resource_type = resource_type
            record.resource_code = resource_code
            record.remark = desc
            db.session.commit()
            res = { 'code': 20000 }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to update resource. Please drop email to yw@sunmi.com'
            }
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify(res)

    def delete(self, *args, **kwargs):
        try:
            resource_id = request.args.get('id')
            record = Resources.query.filter_by(id=resource_id).first()
            db.session.delete(record)
            db.session.commit()
            res = { 'code': 20000 }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to  resource. Please drop email to yw@sunmi.com'
            }
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify(res)


@ns.route('/pms/resource&app/', endpoint='resource&app', methods=['GET', ])
class ResourceWithApp(Resource):
    """
    根据app_id查询Resource
    """
    def get(self, *args, **kwargs):
        try:
            app_id = request.args.get('app_id')
            records = Resources.query.filter_by(app_id=app_id)
            res = {
                'code': 20000,
                'data': resource_schema.dump(records)
            }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to query resource. Please drop email to yw@sunmi.com'
            }
        finally:
            db.session.close()
        return jsonify(res)



@ns.route('/pms/resource_menu&app/', endpoint='resource_menu&app', methods=['GET', ])
class MenuResourceWithApp(Resource):
    """
    根据App ID获取 Menu
    """
    def get(self, *args, **kwargs):
        try:
            app_id = request.args.get('app_id')
            record = ResourceMenu.query.filter_by(app_id=app_id)
            res = {
                'code': 20000,
                'data': resource_menu_schema.dump(record)
            }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to query menu. Please drop email to yw@sunmi.com'
            }
        finally:
            db.session.close()
        return jsonify(res)


@ns.route('/pms/resource_menu/', endpoint='resource_menu', methods=['GET', 'POST', 'PUT', 'DELETE'])
class MenuResource(Resource):
    def get(self, *args, **kwargs):
        try:
            menu_id = request.args.get('id')
            if menu_id == '':
                record = ResourceMenu.query.all()
            else:
                record = ResourceMenu.query.filter_by(id=menu_id)

            res = {
                'code': 20000,
                'data': resource_menu_schema.dump(record)
            }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to query menu. Please drop email to yw@sunmi.com'
            }
        finally:
            db.session.close()
        return jsonify(res)

    def post(self):
        try:
            json_data = request.get_json()
            app_id = json_data['app_id']
            desc = json_data['desc']
            menu_data = json_data['menu_data']
            record = ResourceMenu(app_id=app_id, description=desc, r_menu_data=menu_data)
            db.session.add(record)
            db.session.commit()
            res = { 'code': 20000 }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to add menu. Please drop email to yw@sunmi.com'
            }
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify(res)

    def put(self):
        try:
            json_data = request.get_json()
            menu_id = json_data['menu_id']
            desc = json_data['desc']
            menu_data = json_data['menu_data']
            record = ResourceMenu.query.filter_by(id=menu_id).first()
            record.description = desc
            record.r_menu_data = menu_data
            db.session.commit()
            res = { 'code': 20000 }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to update menu. Please drop email to yw@sunmi.com'
            }
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify(res)

    def delete(self, *args, **kwargs):
        try:
            menu_id = request.args.get('id')
            record = ResourceMenu.query.filter_by(id=menu_id).first()
            db.session.delete(record)
            db.session.commit()
            res = { 'code': 20000 }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to delete menu. Please drop email to yw@sunmi.com'
            }
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify(res)


@ns.route('/pms/menu_unique_check/',endpoint="menu_unique_check",methods=['GET'])
class MenuUniqueCheck(Resource):
    def get(self, *args, **kwargs):
        try:
            app_id = request.args.get('app_id')
            total = ResourceMenu.query.filter_by(app_id=app_id).count()
            if total == 0:
                result = 0
            else:
                result = 1
            res = {
                'code': 20000,
                'data': result
            }
        except Exception as e:
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to query Menu. Please drop email to yw@sunmi.com'
            }
            current_app.logger.error(str(e))
        finally:
            db.session.close()
        return jsonify(res)