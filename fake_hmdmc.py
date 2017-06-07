#!/usr/bin/env python

"""
Very simple listener to receive GET requests for validating HMDMCs.
Perform GET validate?hmdmc=17_000 to see it work.
"""

import argparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import re
from ConfigParser import ConfigParser

class Handler(BaseHTTPRequestHandler):
    PATTERN = re.compile(r'^/?validate\?hmdmc=(.+)$', re.I)
    def do_GET(self):
        path = self.path.upper()
        m = Handler.PATTERN.match(self.path)
        if m:
            hmdmc = m.group(1)
            result = Handler.hmdmcs.get(hmdmc)
            if result is None:
                result = Handler.hmdmcs.get('default', 404)
            result = int(result)
        else:
            result = 404
        self.send_response(result)

def read_file(filename):
    config = ConfigParser()
    config.read(filename)
    return config.defaults()
        
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('port', type=int)
    parser.add_argument('-f', '--file', default='HMDMCs.txt',
        help="File to read HMDMCs from (default is HMDMCs.txt)")
    args = parser.parse_args()
    hmdmcs = read_file(args.file)
    Handler.hmdmcs = hmdmcs
    server = HTTPServer(('0.0.0.0', args.port), Handler)
    try:
        print "Listening on port %s ..."%args.port
        server.serve_forever()
    finally:
        print "Closing"
        server.socket.close()

if __name__=='__main__':
    main()
