import pymysql
import json
from datetime import date, datetime

DB_HOST = 'localhost'
DB_USER = 'smy'
DB_PASS = 'boost'
DB_SCHEMA = 'test'
SERVER_TABLE_COLUMNS = ('id', 'host', 'port', 'anonymous_type', 'type', 'region', 'is_valid', 'validate_time', 'join_time')

def _connect_db():
    return pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_SCHEMA, use_unicode=True, charset='utf8')

def _inflate(keys, row):
    return dict(zip(keys, row))

def _exec_query(sql, args, keys):
    with _connect_db() as c:
        c.execute(sql, args)
        return [_inflate(keys, row) for row in c.fetchall()]

def _exec_update(sql, args):
    conn = _connect_db()
    with conn.cursor() as c:
        c.execute(sql, args)
    conn.commit()
    conn.close()
    
def get_server(types=None, skip=None, limit=None, anonymous=None):
    sql = 'SELECT * FROM server'
    args = []
    if types:
        or_clause = ' OR '.join(["type='%s'" % t for t in types])
        sql += ' WHERE (%s)' % or_clause

    if anonymous is not None:
        if types: sql += ' AND'
        else: sql += ' WHERE'

        if anonymous: sql += " anonymous_type LIKE '%%匿%%'"
        else: sql += " anonymous_type NOT LIKE '%%匿%%'"

    if limit:
        sql += ' LIMIT %s'
        args.append(limit)

        if skip:
            sql += ' OFFSET %s'
            args.append(skip)
            
    return _exec_query(sql, args, SERVER_TABLE_COLUMNS)

def get_server_qty():
    return _exec_query('SELECT count(*) FROM server', None, ('count',))[0]['count']

def update_server(host, _type, is_valid):
    if _type:
        args = (_type, is_valid, host)
        sql = 'UPDATE server SET type=%s, is_valid=%s, validate_time=CURRENT_TIMESTAMP WHERE host=%s'
    else:
        args = (is_valid, host)
        sql = 'UPDATE server SET is_valid=%s, validate_time=CURRENT_TIMESTAMP WHERE host=%s'

    _exec_update(sql, args)
        

class ExternJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)
    
def json_dumps(obj):
    return json.dumps(obj, cls=ExternJsonEncoder)
