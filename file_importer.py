#!/usr/bin/env python3

import sys
import common

if len(sys.argv) < 2:
    print('missing file path', file=sys.stderr)
    exit(1)

def process(line):
    line = line.strip()
    ip, port = line.split(':')
    try:
        common.create_server(ip, port, '匿名', 'http')
    except Exception as e:
        print(e)
        
file = sys.argv[1]
with open(file) as f:
    for line in f.readlines():
        process(line)
