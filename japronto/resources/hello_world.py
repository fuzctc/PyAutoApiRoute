# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Zhichang Fu
# Created Time: 2018-12-13 20:21:11
'''
BEGIN
function:
        
must have param:
        
optional  param:
        
return:
    code:0 success
END
'''

import json


class HelloWorld(object):
    @staticmethod
    def get(request):
        return request.Response(json.dumps({"hello": "world"}))
