#!/usr/bin/env python3
from flask import Flask, request
import db
import json
import checker

app = Flask(__name__)

@app.route('/vpn', methods=['POST'])
def new_vpn():
    host = request.args.get('host')
    port = request.args.get('port')
    db.new_unchecked(dict(host=host, port=port))
    return 'ok'

@app.route('/vpn')
def get_a_vpn():
    vpn = db.get_enable()
    return json.dumps(vpn)

if __name__ == '__main__':
    checker.start()
    app.run('0.0.0.0', port=80, debug=True)
