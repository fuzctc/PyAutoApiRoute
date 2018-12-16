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

import tornado
import tornado.web
import time


class HelloWorld(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        yield time.sleep(5)
        self.write("Hello, world")
        self.finish()
