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

import tornado.web


class HelloWorldPython(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world python")
