# !/usr/bin/python  
# -*- coding:utf-8 -*-
# Author: Zhichang Fu
# Created Time: 2018-12-14 13:52:18
'''
BEGIN
function:
    Config
END
'''

import os


DEBUGVAL = os.environ.get("DEBUG", False)
DEBUG = DEBUGVAL == str(True) if isinstance(DEBUGVAL, str) else bool(DEBUGVAL)
