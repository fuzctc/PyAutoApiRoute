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

from flask_restful import Resource


class HelloWorldPythonTest(Resource):
    def get(self):
        return {"hello": "hello world python"}
