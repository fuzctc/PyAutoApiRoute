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
from japronto import Application
import argparse
import sys
sys.path.append("..")
from base import config, route

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="app running port", type=int, default=8080)
parser.add_argument("--workers", help="worker processes", type=int, default=1)
parse_args = parser.parse_args()

app = Application()
r = app.router

route_path = "./resources"
route_list = route(
    route_path, resources_name="resources", route_prefix="japronto/")

for item in route_list:
    r.add_route(item[0], item[1].get, methods=["GET"])

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(parse_args.port),
        debug=config.DEBUG,
        worker_num=int(parse_args.workers))
