#!/usr/bin/env python3
from flask import Flask, request
import common
from common import json_dumps

app = Flask(__name__)

AVAILABLE_PROXY_TYPE = ['HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5', 'SOCKS']

FAILED = 1
SUCCESS = 0

def msg(ret, _msg):
    return dict(ret=ret, msg=_msg)

def json_msg(ret, _msg):
    return json_dumps(msg(ret, _msg))

def is_notnull(arg):
    return arg is not None

def is_str(arg):
    return isinstance(arg, str)

def is_notnull_str_number(arg):
    return is_notnull(arg) and is_str(arg) and arg.isdecimal()

def is_str_number(arg):
    return is_str(arg) and arg.isdecimal()

# GET /vpn/http-https?page=()&pagesize=()&anonymous=(0/1)
@app.route('/vpn/<_type>')
def get_vpn(_type):
    types = _type.split('-')
    for t in types:
        if t.upper() not in AVAILABLE_PROXY_TYPE:
            return json_msg(FAILED, 'unsupported proxy type')

    page = request.args.get('page')
    if not page: page = 0
    elif not is_str_number(page): return json_msg(FAILED, 'argument "page" error: %s' % page)
    else: page = int(page)

    pagesize = request.args.get('pagesize')
    if not pagesize: pagesize = 50
    elif not is_str_number(pagesize): return json_msg(FAILED, 'argument "anonymous" error: %s' % pagesize)
    else: pagesize = int(pagesize)

    anonymous = request.args.get('anonymous')
    if not anonymous: anonymous = None
    elif not is_str_number(anonymous): return json_msg(FAILED, 'argument "anonymous" error: %s' % anonymous)
    elif int(anonymous) == 1: anonymous = True
    else: anonymous = False

    ret = msg(SUCCESS, 'ok')
    ret['servers'] = common.get_server(types, page * pagesize, pagesize, anonymous)
    ret['total'] = common.get_server_qty() # todo: 根据参数返回对应类型的数量
    return json_dumps(ret)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

    
