# -*- coding:utf-8 -*-
from app.models import PermissionMenu, ResourceMenu
from app.models import db

def arrToRouter(p_menu_id):
    pro = PermissionMenu.query.get(p_menu_id)
    checked_keys = pro.checked_keys
    res_menu_id = pro.res_menu_id

    # menu的json数据
    menu_list = []
    checked_keys_list = []
    r_menu_pro = ResourceMenu.query.get(res_menu_id)
    r_menu_data = r_menu_pro.r_menu_data

    for data in r_menu_data:
        for key in checked_keys:
            if key == data['id'] and 'pid' in data and data['pid'] not in checked_keys_list:
                checked_keys_list.append(data['pid'])
            if key not in checked_keys_list:
                checked_keys_list.append(key)
    for data in r_menu_data:
        for key in checked_keys_list:
            if data['id'] == key:
                menu_list.append(data)

    # 将json数据转换为router
    data_list = []
    for menu in menu_list:
        item_dict = {}
        item_dict['id'] = menu['id']
        if 'pid' in menu:
            item_dict['pid'] = menu['pid']
        item_dict['redirect'] = menu['meta']['redirect']
        item_dict['path'] = menu['meta']['path']
        item_dict['component'] = menu['meta']['component']
        item_dict['hidden'] = menu['meta']['hidden']
        item_dict['name'] = menu['meta']['name']
        item_dict['meta'] = {'title': menu['meta']['title'], 'icon': menu['meta']['icon']}
        data_list.append(item_dict)

    # 将数据存储为 以 id 为 KEY 的 map 索引数据列
    map = {}
    for menu in data_list:
        map[menu['id']] = menu

    #更新checked_keys
    for key in checked_keys:
        if key not in map:
            checked_keys.remove(key)
    pro.checked_keys = checked_keys
    db.session.commit()
    # db.session.close()


    #判断父级，加入children
    val = []
    for menu in data_list:
        if 'pid' not in menu:
            del menu['id']
            val.append(menu)
        else:
            parent = map[menu['pid']]
            if 'children' in parent.keys():
                parent['children'].append(menu)
                del menu['id']
                del menu['pid']
            else:
                parent['children'] = []
                parent['children'].append(menu)
                del menu['id']
                del menu['pid']
    return val