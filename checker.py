#!/usr/bin/env python3
import urllib
from urllib.request import Request
import socks
import functools
import concurrent
import common
from concurrent.futures import ThreadPoolExecutor

TRY_HOST = 'http://www.baidu.com'
HTTP_TIMEOUT = 10
    
def validate_http(host, port):
    req = Request(TRY_HOST)
    req.set_proxy('%s:%s' % (host, port), 'http')
    try:
        rsp = urllib.request.urlopen(req, timeout=HTTP_TIMEOUT)
    except Exception as e:
        return False
    else:
        return rsp.status == 200

def validate_socks(_type, host, port):
    s = socks.socksocket()
    s.set_proxy(_type, host, port)
    s.settimeout(10)
    try:
        s.connect((TRY_HOST, 80))
    except Exception as e:
        return False
    return True
 
validate_socks4 = functools.partial(validate_socks, socks.SOCKS4)
validate_socks5 = functools.partial(validate_socks, socks.SOCKS5)

def validate(server):
    if not server['host'] or not server['port']:
        return False
    
    if server['type']: _try_order = [server['type'].upper()]
    elif server['port'] in [80, 8080, 3128, 8081, 9080, 8888]: _try_order = ['HTTP']
    elif server['port'] == 443: _try_order = ['HTTPS']
    elif server['port'] == 1080: _try_order = ['SOCKS4', 'SOCKS5']
    else: _try_order = ['HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5']

    for t in _try_order:
        if t in ('HTTP', 'HTTPS'):
            if validate_http(server['host'], server['port']):
                common.update_server(server['host'], t, True)
                print('valid: %s:%s' % (server['host'], server['port']))
                return True
        elif t in ['SOCKS4', 'SOCKS4/5']:
            if validate_sock4(server['host'], server['port']):
                common.update_server(server['host'], t, True)
                print('valid: %s:%s' % (server['host'], server['port']))
                return True
        elif t == 'SOCKS5':
            if validate_sock5(server['host'], server['port']):
                common.update_server(server['host'], t, True)
                print('valid: %s:%s' % (server['host'], server['port']))
                return True
        else:
            print('unknow type: %s' % t)
            return False

    common.update_server(server['host'], None, False)
    print('invalid: %s:%s' % (server['host'], server['port']))
            
def start():
    skip = 0
    limit = 100
    total = common.get_server_qty()
    pool = ThreadPoolExecutor(40)
    futures = []
    while skip < total:
        servers = common.get_server(skip=skip, limit=limit)
        for server in servers:
            futures.append(pool.submit(validate, server))
        skip += len(servers)

    concurrent.futures.wait(futures)

if __name__ == '__main__':
    start()
