# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Zhichang Fu
# Created Time: 2018-12-14 11:13:31
'''
BEGIN
function:
    Automatic map routing
END
'''

import re
import os
#import importlib
from . import config


def hump_to_underline(hunp_str):
    '''
    驼峰形式字符串转成下划线形式
    Hump form string is converted to underline form
    :param hunp_str: 驼峰形式字符串 hump form string
    :return: underline form string
    '''
    p = re.compile(r'([a-z]|\d)([A-Z])')
    sub = re.sub(p, r'\1_\2', hunp_str).lower()
    return sub


def underline_to_hump(underline_str):
    '''
    下划线形式字符串转成驼峰形式
    Underline form stirng is converted to hump form
    :param underline_str: 下划线形式字符串 underline form stirng
    :return: 驼峰形式字符串 hump form stirng
    '''
    sub = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), underline_str)
    if len(sub) > 1:
        return sub[0].upper() + sub[1:]
    return sub


def import_object(name):
    # type: (_BaseString) -> Any
    """Imports an object by name.

    import_object('x') is equivalent to 'import x'.
    import_object('x.y.z') is equivalent to 'from x.y import z'.
    """
    if not isinstance(name, str):
        name = name.encode('utf-8')
    if name.count('.') == 0:
        return __import__(name, None, None)

    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError("No module named %s" % parts[-1])


def route(route_file_path,
          resources_name="resources",
          route_prefix="",
          existing_route=None):
    """
    Automatic import of modules and map routing
    根据接口文件夹自动导入模块和映射路由
    :param route_file_path: Api interface folder path API接口文件地址
    :param resources_name: Api folder module name, default `resources`
                           API接口文件模块名称，默认为 resources
    :param route_prefix: route prefix, default None 路由前缀，默认为空
    :param existing_route: if exist an irregular routing definition, 
    you need to pass this parameter. And Must be in dictionary format.
        example:
            exists route: /getHelloWorldInfo
            required route format: /get_hello_world_info
            so:
              existing_route = {"/get_hello_world_info": "/getHelloWorldInfo"}
    如果存在未按规范要求的路由，则需要传此参数，且此参数必须是字典格式.
    :return route_list:
        Returns an array containing tuples, the tuple content is
        `(Route endpoint, Request Class)`. The first parameter is the routing
        path, the second parameter is the request class object for this route.
        返回一个数组，里面是多个元组，元组的内容是第一个参数是路由地址，
        第二个参数是此路由的请求类对象
    """
    route_list = []

    def get_route_tuple(file_name, route_pre, resource_module_name):
        """
        :param file_name: API file name
        :param route_pre: route prefix
        :param resource_module_name: resource module
        """
        nonlocal route_list
        nonlocal existing_route
        route_endpoint = file_name.split(".py")[0]
        #module = importlib.import_module('{}.{}'.format(
        #    resource_module_name, route_endpoint))
        module = import_object('{}.{}'.format(
            resource_module_name, route_endpoint))
        route_class = underline_to_hump(route_endpoint)
        real_route_endpoint = r'/{}{}'.format(route_pre, route_endpoint)
        if existing_route and isinstance(existing_route, dict):
            if real_route_endpoint in existing_route:
                real_route_endpoint = existing_route[real_route_endpoint]
        route_list.append((real_route_endpoint, getattr(module, route_class)))

    def check_file_right(file_name):
        if file_name.startswith("_"):
            return False
        if not file_name.endswith(".py"):
            return False
        if file_name.startswith("."):
            return False
        return True

    def recursive_find_route(route_path, sub_resource, route_pre=""):
        nonlocal route_prefix
        nonlocal resources_name
        file_list = os.listdir(route_path)
        if config.DEBUG:
            print("FileList:", file_list)
        for file_item in file_list:
            if file_item.startswith("_"):
                continue
            if file_item.startswith("."):
                continue
            if os.path.isdir(route_path + "/{}".format(file_item)):
                recursive_find_route(route_path + "/{}".format(file_item),
                                     sub_resource + ".{}".format(file_item),
                                     "{}{}/".format(route_pre, file_item))
                continue
            if not check_file_right(file_item):
                continue
            get_route_tuple(file_item, route_prefix + route_pre, sub_resource)

    recursive_find_route(route_file_path, resources_name)
    if config.DEBUG:
        print("RouteList:", route_list)

    return route_list
