from flask_restplus import Resource
from app.api import ns
from flask import request, jsonify, current_app
from app.models import db
from sqlalchemy import and_, or_
from app.marshalling import permission_menu_schema
from app.models import Permission, Resources, Application, PermissionMenu, ResourceMenu
from app.utils import mapPerm
import json

@ns.route('/pms/permission/', endpoint='permission', methods=['POST', 'DELETE', 'PUT', 'GET'])
class PermissionApi(Resource):
    def get(self, *args, **kwargs):
        my_form= request.args.get('form')
        query  = json.loads(my_form)
        if query['resource_id'] == '' and query['app_id'] =='':
            count = Permission.query.count()
            projects = Permission.query.order_by(
                        Permission.id
                        ).paginate(query['page'], query['limit'], error_out=False)
        elif query['resource_id'] == '' and query['app_id'] !='':
            count = Permission.query.filter_by(app_id=query['app_id']).count()
            projects = Permission.query.filter_by(app_id=query['app_id']).order_by(
                        Permission.id
                        ).paginate(query['page'], query['limit'], error_out=False)
        else:
            count = Permission.query.filter(Permission.resource_id==query['resource_id']).count()
            projects = Permission.query.filter(Permission.resource_id==query['resource_id']
                        ).order_by(
                        Permission.id
                        ).paginate(query['page'], query['limit'], error_out=False)
        pms_list = []
        data = []
        for pro in projects.items:
            item_dict = {}
            item_dict['id'] = pro.id
            item_dict['remark'] = pro.remark
            item_dict['permission_name'] = pro.permission_name
            item_dict['app_id'] = pro.app_id
            app_pro = Application.query.get(pro.app_id)
            item_dict['app_name'] = app_pro.app_name
            resource_pro = Resources.query.get(pro.resource_id)
            item_dict['resource_name'] = resource_pro.resource_name
            item_dict['resource_type'] = resource_pro.resource_type
            item_dict['resource_id'] = resource_pro.id
            perms = mapPerm.map_perm(pro.action, resource_pro.resource_type)
            if perms == []:
                item_dict['action'] = [0]
                item_dict['action_list'] = ['DISABLE']
            else:
                action_list = []
                for perm in perms:
                    if perm == 'DELETE':
                        action_v = 8
                    if perm == 'PUT':
                        action_v = 4
                    if perm == 'POST':
                        action_v = 2
                    if perm == 'GET':
                        action_v = 1
                    action_list.append(action_v)
                item_dict['action_list'] = perms
                item_dict['action'] = action_list
            pms_list.append(item_dict)
        data.append(pms_list)
        res = {
            'code': 20000,
            'data': data,
            'total': count
        }
        db.session.close()
        return jsonify(res)

    def post(self):
        try:
            json_data = request.get_json()
            resource_id = json_data['form']['resource_id']
            resource_pro = Resources.query.get(resource_id)
            app_id = json_data['form']['app_id']
            app_pro = Application.query.get(app_id)
            action = json_data['form']['action']
            action_value = sum(action)
            perms = mapPerm.map_perm(action_value, resource_pro.resource_type)
            if perms == []:
                aciton_str = 'DISABLE'
            else:
                aciton_str = ('-').join(perms)
            remark = app_pro.app_name + '-' + resource_pro.resource_name + '-' + resource_pro.resource_type + '-' + aciton_str
            permission_name = resource_pro.resource_name + '-' + bin(action_value)
            pms_count = Permission.query.filter(and_(Permission.resource_id==resource_id, Permission.action==action_value)).count()
            if pms_count != 0:
                res = {
                    'code': 50000,
                    'message':  'ERROR: Permission is already exists!'
                }
                return jsonify(res)
            else:
                record = Permission(app_id=app_id, resource_id=resource_id, action=action_value, remark=remark, permission_name=permission_name)
                db.session.add(record)
                db.session.commit()
                res = {'code': 20000, }

        except Exception as e:
            current_app.logger.info("ERROR:" + str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to add permission. Please drop email to yw@sunmi.com'
            }
            db.session.rollback()
        finally:
            db.session.close()

        return jsonify(res)

    def put(self):
        try:
            json_data = request.get_json()
            pms_id = json_data['form']['id']
            pro = Permission.query.filter_by(id=pms_id).first()
            resource_id = json_data['form']['resource_id']
            resource_pro = Resources.query.get(resource_id)
            app_id = json_data['form']['app_id']
            app_pro = Application.query.get(app_id)
            action = json_data['form']['action']
            action_value = sum(action)
            perms = mapPerm.map_perm(action_value, resource_pro.resource_type)
            if perms == []:
                aciton_str = 'DISABLE'
            else:
                aciton_str = ('-').join(perms)
            pms_count = Permission.query.filter(and_(Permission.resource_id==resource_id, Permission.action==action_value)).count()
            if pms_count != 0:
                res = {
                    'code': 50000,
                    'message':  'ERROR: Permission is already exists!'
                }
                return jsonify(res)
            # Update Template Type
            else:
                pro.action = action_value
                pro.permission_name = resource_pro.resource_name + '-' + bin(action_value)
                pro.remark = app_pro.app_name + '-' + resource_pro.resource_name + '-' + resource_pro.resource_type + '-' + aciton_str
                db.session.commit()
                res = {'code': 20000}
        #
        except Exception as e:
            current_app.logger.info("ERROR:" + str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to update permission. Please drop email to yw@sunmi.com'
            }
            db.session.rollback()
        finally:
            db.session.close()

        return jsonify(res)

    def delete(self):
        try:
            pms_id = request.args.get('id')
            record = Permission.query.get(pms_id)
            #record.logic_del = 0
            db.session.delete(record)
            db.session.commit()
            res = {'code': 20000}

        except Exception as e:
            current_app.logger.info("ERROR:" + str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to delete permission. Please drop email to yw@sunmi.com'}
            db.session.rollback()
        finally:
            db.session.close()

        return jsonify(res)

@ns.route('/pms/perm_menu/', endpoint='perm_menu', methods=['POST', 'DELETE', 'PUT', 'GET'])
class PermMenuApi(Resource):
    def get(self, *args, **kwargs):
        my_form= request.args.get('form')
        query  = json.loads(my_form)
        if query['app_id'] =='':
            count = PermissionMenu.query.count()
            projects = PermissionMenu.query.order_by(
                         PermissionMenu.id
                        ).paginate(query['page'], query['limit'], error_out=False)
        else:
            count = PermissionMenu.query.filter_by(app_id=query['app_id']).count()
            projects = PermissionMenu.query.filter_by(app_id=query['app_id']).order_by(
                           PermissionMenu.id
                        ).paginate(query['page'], query['limit'], error_out=False)
        res = {
            'code': 20000,
            'data': permission_menu_schema.dump(projects.items),
            'total': count
        }
        db.session.close()
        return jsonify(res)

    def post(self):
        try:
            json_data = request.get_json()
            app_id = json_data['form']['app_id']
            p_menu_name = json_data['form']['p_menu_name']
            description = json_data['form']['description']
            checked_keys = json_data['form']['checked_keys']
            res_menu_pro = ResourceMenu.query.filter_by(app_id=app_id).first()
            r_menu_id = res_menu_pro.id

            #判断菜单权限名称和菜单权限router是否存在，如果存在，返回异常，正常则添加数据。
            pms_count = PermissionMenu.query.filter_by(p_menu_name=p_menu_name).count()
            if pms_count != 0:
                res = {
                    'code': 50000,
                    'message':  'ERROR: PermissionMenu is already exists!'
                }
            else:
                record = PermissionMenu(app_id=app_id, res_menu_id=r_menu_id, p_menu_name=p_menu_name, checked_keys=checked_keys, description=description )
                db.session.add(record)
                db.session.commit()
                res = {'code': 20000, }

        except Exception as e:
            current_app.logger.info("ERROR:" + str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to add PermissionMenu. Please drop email to yw@sunmi.com'
            }
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify(res)

    def put(self):
        try:
            json_data = request.get_json()
            description = json_data['form']['description']
            p_menu_id = json_data['form']['id']
            pro = PermissionMenu.query.get(p_menu_id)
            checked_keys = json_data['form']['checked_keys']

            pms_count = PermissionMenu.query.filter_by(checked_keys=checked_keys).count()
            if pms_count != 0:
                res = {
                    'code': 50000,
                    'message':  'ERROR: PermissionMenu is already exists!'
                }
            # Update P_menu
            else:
                pro.checked_keys = checked_keys
                pro.description = description
                db.session.commit()
                res = {'code': 20000}

        except Exception as e:
            current_app.logger.info("ERROR:" + str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to update PermissionMenu. Please drop email to yw@sunmi.com'
            }
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify(res)

    def delete(self):
        try:
            pms_id = request.args.get('id')
            record = PermissionMenu.query.get(pms_id)
            db.session.delete(record)
            db.session.commit()
            res = {'code': 20000}

        except Exception as e:
            current_app.logger.info("ERROR:" + str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to delete PermissionMenu. Please drop email to yw@sunmi.com'}
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify(res)

@ns.route('/pms/perm_menu&app/', endpoint='perm_menu&app', methods=['GET', ])
class PermMenuWithApp(Resource):
    def get(self, *args, **kwargs):
        try:
            app_id = request.args.get('app_id')
            record = PermissionMenu.query.filter_by(app_id=app_id)
            res = {
                'code': 20000,
                'data': permission_menu_schema.dump(record)
            }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to get permission menu. Please drop email to yw@sunmi.com'
            }
        finally:
            db.session.close()
        return jsonify(res)