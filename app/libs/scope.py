# -*- encoding: utf-8 -*-
"""
@File Name      :   scope.py    
@Create Time    :   2021/7/13 10:00
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

sun_module_name = 'sun.'

api_module_name = 'api.'

version_v1_0_name = 'v1_0.'

user_module_name = 'user.'


# scope基类
class BaseScope:
    allow_apis = []
    # 除了直接写完整的api，还可以指定某个模块
    allow_modules = []
    # 用于排除模块内的一些api，减少配置的代码
    # attention:forbidden_apis必须要和allow_modules一起搭配使用
    forbidden_apis = []

    # 可以使用__add__()重载+运算符
    # attention:相加就类似于数学上的并集
    def add(self, other):
        self.allow_apis += other.allow_apis
        self.allow_apis = list(set(self.allow_apis))
        self_forbidden_apis_copy = self.forbidden_apis
        other_forbidden_apis_copy = other.forbidden_apis
        for i in other.forbidden_apis:
            find = False
            for j in self.allow_modules:
                if i.startswith(j):
                    find = True
                    break
            if find:
                other_forbidden_apis_copy.remove(i)
        for i in self.forbidden_apis:
            find = False
            for j in other.allow_modules:
                if i.startswith(j):
                    find = True
                    break
            if find:
                self_forbidden_apis_copy.remove(i)
        new_forbidden_apis = self_forbidden_apis_copy + other_forbidden_apis_copy
        self.forbidden_apis = list(set(new_forbidden_apis))
        self.allow_modules += other.allow_modules
        self.allow_modules = list(set(self.allow_modules))

    # 在知道两个作用域毫无相关的时候可以不判断作用域是否有交集，减少不必要的计算
    def simple_add(self, other):
        self.allow_apis += other.allow_apis
        self.allow_apis = list(set(self.allow_apis))
        self.forbidden_apis += other.forbidden_apis
        self.forbidden_apis = list(set(self.forbidden_apis))
        self.allow_modules += other.allow_modules
        self.allow_modules = list(set(self.allow_modules))
        return self


class UserScope(BaseScope):
    allow_apis = []
    allow_modules = ['sun.api.v1_0.login', 'sun.api.v1_0.file', 'sun.api.v1_0.dataset', 'sun.api.v1_0.project',
                     'sun.api.v1_0.analysis']

    def __init__(self):
        pass


class AdminScope(BaseScope):
    allow_apis = []
    allow_modules = ['sun.api.v1_0']

    def __init__(self):
        super().__init__(self)


class SuperAdminScope(BaseScope):
    allow_apis = []

    def __init__(self):
        super().__init__(self)
        self.add(AdminScope())


def is_in_scope(scopes, endpoint):
    # 这里用到了flask2.0的蓝图嵌套机制
    # 因为python并没有反射这个机制，所以需要使用globals()
    gl = globals()
    # 在多个角色中查询权限
    for scope in scopes:
        scope = gl[scope]()
        # 先判断URL是否被禁止了
        if endpoint in scope.forbidden_apis:
            return False
        if endpoint in scope.allow_apis:
            return True
        for i in scope.allow_modules:
            if endpoint.startswith(i):
                return True
        return False
