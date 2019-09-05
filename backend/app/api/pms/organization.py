# -*- coding:utf-8 -*-
from flask import current_app,request,jsonify
from flask_restplus import Resource,fields as filed
from app.api import ns
from app.models import db,Group,User,Permission
from app.marshalling import gma,group_schema,groups_schema
from app.utils.map_perm import mapPerm

# 给swagger用
class Model(object):
    group_model = ns.model('填写组信息', {
        'group_name': filed.String,
        'app_id':filed.Integer,
        'remark': filed.String
    })

# 获取用户列表作为穿梭框选项
@ns.route('/pms/users/',endpoint='users_data',methods=['GET','POST'])
class GetUsers(Resource):
    def post(self):
        """
        获取用户，格式化key,value
        """
        json_data = request.get_json()
        group_id = json_data['group_id']
        users = User.query.all()
        users_data = []
        users_selected = []
        group = Group.query.filter_by(id=group_id).first()
        # 组成员，作为已选择项渲染
        for user in group.users:
            users_selected.append(user.id)

        # 所有用户作为待选项，穿梭框组件会根据已选择的id自动取差集
        for user  in  users:
            users_data.append({"key":user.id,"label":"%s-%s" % (user.username,user.code) })

        db.session.commit()
        data = {
            'code': 20000,
            'data':[users_data,users_selected]
        }
        return gma.dump(data)

# 获取指定系统的权限列表作为穿梭框选项
@ns.route('/pms/perms/',endpoint='perms_data',methods=['GET','POST'])
class GetPerms(Resource):
    def post(self):
        """
        获取权限，格式化key,value
        """
        json_data = request.get_json()
        group_id = json_data['group_id']
        group = Group.query.filter_by(id=group_id).first()
        # 组权限，作为已选择项渲染
        perms_selected = []
        for perm in group.permissions:
            perms_selected.append(perm.id)

        # 指定系统下的权限为待选项，穿梭框组件会根据已选择的id自动取差集
        app_id = group.app_id
        perms = Permission.query.filter_by(app_id=app_id)
        perms_data = []
        for perm  in  perms:
            perms_data.append({"remark":perm.remark,"key":perm.id,"label":perm.permission_name, "resource_name":perm.resource.resource_name })

        db.session.commit()
        data = {
            'code': 20000,
            'data':[perms_data,perms_selected]
        }

        return gma.dump(data)

# 组操作
@ns.route('/pms/group/',endpoint="group",methods=['GET','POST','PUT','DELETE'])
class GroupView(Resource):
    def get(self):
        """
        获取组列表
        """
        groups = Group.query.all()
        result = groups_schema.dump(groups)
        db.session.commit()
        data = {
            'code': 20000,
            'data': result
        }
        current_app.logger.info('获取组列表')
        return gma.dump(data)

    @ns.doc(body=Model.group_model, desciption='填写组信息')
    def post(self):
        """
        创建组
        """
        json_data = request.get_json()
        group_name = json_data['group_name']
        remark = json_data['remark']
        app_id = json_data['app_selected']
        try:
            group = Group(group_name = group_name,remark = remark,app_id=app_id)
            db.session.add(group)
            result = "组创建成功"
        except Exception as e:
            db.session.rollback()
            result = "创建失败：%s" % str(e)
        finally:
            db.session.commit()
            db.session.close()
        data = {
            'code': 20000,
            'data': result
        }
        return gma.dump(data)

    def put(self):
        try:
            json_data = request.get_json()
            id = json_data['id']
            act = json_data['act']

            if act == 'users':
                """
                设置组成员
                """
                users = json_data['selected']
                group_users = []
                group = Group.query.filter_by(id=id).first()
                for user_id in users:
                    user = User.query.filter_by(id=user_id).first()
                    if user:
                        group_users.append(user)
                group.users = group_users

            if act == 'perms':
                """
                设置组权限
                """
                perms = json_data['selected']
                group_perms = []
                group = Group.query.filter_by(id=id).first()
                for perm_id in perms:
                    perm = Permission.query.filter_by(id=perm_id).first()
                    if perm:
                        group_perms.append(perm)
                group.permissions = group_perms

            if act == 'menu':
                perm_menu = json_data['selected']
                group = Group.query.filter_by(id=id).first()
                if perm_menu == '':
                    group.perm_menu_id = None
                else:
                    group.perm_menu_id = perm_menu

            db.session.commit()
            data = {
                'code': 20000,
                'data': '设置成功'
            }
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e))
            data = {
                'code': 50000,
                'message': 'Failed to update menu. Please drop email to yw@sunmi.com'
            }
        finally:
            db.session.close()
        return gma.dump(data)

    def delete(self):
        """
        删除组
        """
        json_data = request.get_json()
        id = json_data['id']
        group = Group.query.filter_by(id=id).first()
        db.session.delete(group)
        db.session.commit()
        data = {
            'code': 20000,
            'data': '删除成功'
        }
        return gma.dump(data)


@ns.route('/pms/group_unique_check/',endpoint="group_unique_check",methods=['GET'])
class GroupUniqueCheck(Resource):
    def get(self, *args, **kwargs):
        try:
            app_id = request.args.get('app_id')
            group_name = request.args.get('group_name')
            total = Group.query.filter(
                Group.app_id == app_id,
                Group.group_name == group_name
            ).count()
            if total == 0:
                result = 0
            else:
                result = 1

            res = {
                'code': 20000,
                'data': result
            }
        except Exception as e:
            current_app.logger.error(str(e))
            res = {
                'code': 50000,
                'message': 'ERROR: Failed to query Group. Please drop email to yw@sunmi.com'
            }
        finally:
            db.session.close()
        return jsonify(res)
