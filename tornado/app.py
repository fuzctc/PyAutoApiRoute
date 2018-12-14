# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Zhichang Fu
# Created Time: 2018-12-13 20:12:54

import os
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import sys
sys.path.append("..")
from base import route, config

DEBUG = os.environ.get("DEBUG", False)
define('port', default=8000, type=int, help='run server on the given port.')
define('num_processes', default=1, type=int, help='num processes.')

route_path = "./resources"
exist_route_dict = {"/tornado/hello_world": "/tornado/getHelloWorld"}

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        route(
            route_path,
            route_prefix="tornado/",
            existing_route=exist_route_dict),
        debug=config.DEBUG)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, '0.0.0.0')
    http_server.start(num_processes=options.num_processes)
    tornado.ioloop.IOLoop.current().start()
