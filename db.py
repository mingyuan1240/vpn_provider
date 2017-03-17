import os
import redis
import json

r = redis.StrictRedis(host=os.environ['REDIS_PORT_6379_TCP_ADDR'], port=os.environ['REDIS_PORT_6379_TCP_PORT'])

def take_unchecked():
    return json.loads(r.blpop('uncheck')[1].decode('utf-8'))

def new_unchecked(v):
    r.rpush('uncheck', json.dumps(v))

def take_enable():
    return json.loads(r.blpop('enable')[1].decode('utf-8'))

def get_enable():
    v = r.lindex('enable', 0)
    if v:
        v = json.loads(v)
    return v

def tag_checked(v):
    r.sadd('checked', v)

def is_checked(v):
    return r.sismember('checked', v)

def tag_enable(v):
    r.rpush('enable', json.dumps(v))

