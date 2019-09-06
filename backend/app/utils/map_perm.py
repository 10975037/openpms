# -*- coding:utf-8 -*-
class mapPerm:
    @classmethod
    def map_perm(cls,action,type):
        perms = {"data": ["ENABLE"], "element": ["ENABLE"], "url": ['GET', 'POST', 'PUT', 'DELETE']}.get(type)
        for i in range(len(perms), 0, -1):
            res = (action >> (i - 1)) & 1
            if res is 0:
                perms.pop(i - 1)
        return perms
    @classmethod
    def auth_method(cls,method,action):
        methods = {'GET':1,'POST':2,'PUT':3,'DELETE':4}
        flag = methods.get(method)
        if flag:
            perm = ( action >> (flag-1) ) & 1
            if perm is 1:
                return True
        return False
# print(int(0b1000)) #转换结果为8,这里的1没有任何作用，因为element类型只判断最后1位
# perms = mapPerm.map_perm(15,'element')
# print(perms)