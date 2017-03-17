import urllib
from urllib.request import Request
import json
import db
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

TRY_HOST = 'http://httpbin.org/ip'
HTTP_TIMEOUT = 10

CHECKER_THREAD_NUM = 40
    
def validate_http(host, port):
    req = Request(TRY_HOST)
    req.set_proxy('%s:%s' % (host, port), 'http')
    try:
        rsp = urllib.request.urlopen(req, timeout=HTTP_TIMEOUT)
        body = rsp.read().decode('utf-8')
        data = json.loads(body)
        if 'origin' not in data:
            return False        
    except Exception as e:
        return False
    else:
        return rsp.status == 200

def check_unchecked():
    print('start checker thread')
    while True:
        vpn = db.take_unchecked()
        print(vpn)
        if not vpn.get('port'):
            try_ports = [80, 8080, 443, 3128, 8081, 9080, 8888]
        else:
            try_ports = [vpn['port']]

        db.tag_checked(vpn['host'])
        for port in try_ports:
            if validate_http(vpn['host'], port):
                print('%s:%s is usabel' % (vpn['host'], vpn['port']))
                vpn['port'] = port
                db.tag_enable(vpn)

def check_usabled():
    print('start checker usabled thread')
    while True:
        vpn = db.take_enable()
        if validate_http(vpn['host'], vpn['port']):
            db.tag_enable(vpn)
        time.sleep(10)

def start():
    pool = ThreadPoolExecutor(CHECKER_THREAD_NUM)
    for _ in range(CHECKER_THREAD_NUM):
        pool.submit(check_unchecked)

    Thread(target=check_usabled).start()
