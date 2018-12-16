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

from sanic.views import HTTPMethodView
from sanic import response


class HelloWorld(HTTPMethodView):
    def get(self, request):
        return response.json({"hello": "world"})
