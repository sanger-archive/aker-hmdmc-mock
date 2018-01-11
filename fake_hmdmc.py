#!/usr/bin/env python

"""
Very simple listener to receive GET requests for validating HMDMCs.
Perform GET validate?hmdmc=17_000 to see it work.
"""

import argparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import re
import json
from ConfigParser import ConfigParser

import ssl

class Handler(BaseHTTPRequestHandler):
    """Accepts validate?hmdmc=# or /validateHMDMC?hmdmc=#.
    Responds with a 200 as long as the request is correctly formed.
    Sends back JSON with the error code described in the config
    file for that HMDMC code.
    JSON specifies valid=true if the error code is zero, otherwise
    valid=false."""
    PATTERN = re.compile(r'^/?validate(?:hmdmc)?\?hmdmc=(.+)$', re.I)
    def do_GET(self):
        m = Handler.PATTERN.match(self.path)
        if not m:
            self.send_response(404)
            self.end_headers()
            return
        hmdmc = m.group(1)
        errorcode = Handler.hmdmcs.get(hmdmc)
        if errorcode is None:
            errorcode = Handler.hmdmcs.get('default', 0)
        errorcode = int(errorcode)
        data = {
            'valid': (errorcode==0),
            'errorcode': errorcode,
            'productclasses': []
        }
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        json.dump(data, self.wfile)

def read_file(filename):
    config = ConfigParser()
    config.read(filename)
    return config.defaults()

def run_http_server(args, Handler):
    server = HTTPServer(('0.0.0.0', args.port), Handler)
    try:
        print "Listening to HTTP on port %s ..."%args.port
        server.serve_forever()
    finally:
        print "Closing"
        server.socket.close()

def run_https_server(args, Handler):
    server = HTTPServer(('0.0.0.0', args.port), Handler)
    server.socket = ssl.wrap_socket(server.socket, certfile=args.certfile, keyfile=args.keyfile, server_side=True)
    try:
        print "Listening to HTTPS on port %s ..."%args.port
        server.serve_forever()
    finally:
        print "Closing"
        server.socket.close()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('port', type=int)
    parser.add_argument('-f', '--file', default='HMDMCs.txt',
        help="File to read HMDMCs from (default is HMDMCs.txt)")
    parser.add_argument('-c', '--certfile', help="Path to the certificate file to use for HTTPS")
    parser.add_argument('-k', '--keyfile', help="Path to the key file to use with the certificate")

    args = parser.parse_args()
    hmdmcs = read_file(args.file)
    Handler.hmdmcs = hmdmcs

    if (not args.certfile):
        run_http_server(args, Handler)
    else:
        run_https_server(args, Handler)       

if __name__=='__main__':
    main()
