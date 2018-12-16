# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Zhichang Fu
# Created Time: 2018-12-14 14:12:31
'''
BEGIN
function:
    sanic app
return:
    code:0 success
END
'''

from sanic import Sanic
import argparse
import sys
sys.path.append("..")
from base import config, route

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="app running port", type=int, default=8080)
parser.add_argument("--workers", help="app running port", type=int, default=1)
parse_args = parser.parse_args()

app = Sanic("App")

route_path = "./resources"
route_list = route(
    route_path, resources_name="resources", route_prefix="sanic/")

for item in route_list:
    app.add_route(item[1].as_view(), item[0])

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(parse_args.port),
        debug=config.DEBUG,
        workers=int(parse_args.workers))
