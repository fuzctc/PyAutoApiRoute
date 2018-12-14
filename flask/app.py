# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Zhichang Fu
# Created Time: 2018-12-14 14:12:31
'''
BEGIN
function:
    flask app
return:
    code:0 success
END
'''

import argparse
from flask import Flask
from flask_restful import Api
import sys
sys.path.append("..")
from base import config, route

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="app running port", type=int, default=5000)
parse_args = parser.parse_args()

app = Flask(__name__)
api = Api(app)


@app.before_request
def before_request():
    """
    Init runtime parameters and check API token before api request.
    """
    pass


@app.after_request
def after_request(response):
    """
    Send api response log and sql log to log system after api request;
    Session commit after api request.
    :param response: api return request result to the client
    :return: response
    """
    return response


# APi route and processing functions
route_path = "./resources"
route_list = route(route_path, resources_name="resources", route_prefix="")

for item in route_list:
    print(item)
    api.add_resource(item[1], item[0])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(parse_args.port), debug=config.DEBUG)
