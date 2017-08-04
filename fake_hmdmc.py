#!/usr/bin/env python

"""
Very simple listener to receive GET requests for validating HMDMCs.
Perform GET validate?hmdmc=17_000 to see it work.
"""

import argparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import re
from ConfigParser import ConfigParser

import ssl

class Handler(BaseHTTPRequestHandler):
    PATTERN = re.compile(r'^/?validate\?hmdmc=(.+)$', re.I)
    def do_GET(self):
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
        self.end_headers()

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
    server = HTTPServer(('0.0.0.0', args.sslport), Handler)
    server.socket = ssl.wrap_socket(server.socket, certfile=args.certificate, keyfile=args.keyfile, server_side=True)
    try:
        print "Listening to HTTPS on port %s ..."%args.sslport
        server.serve_forever()
    finally:
        print "Closing"
        server.socket.close()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--port', type=int, help="If provided, it will start a http server in the port number specified")
    parser.add_argument('-f', '--file', default='HMDMCs.txt',
        help="File to read HMDMCs from (default is HMDMCs.txt)")
    parser.add_argument('-c', '--certificate', help="Path to the certificate file to use for HTTPS")
    parser.add_argument('-k', '--keyfile', help="Path to the key file to use with the certificate")
    parser.add_argument('-s', '--sslport', type=int, help="If provided, it will start a https server in the port number specified")

    args = parser.parse_args()
    hmdmcs = read_file(args.file)
    Handler.hmdmcs = hmdmcs

    if (args.port):
        run_http_server(args, Handler)

    if (args.sslport):
        run_https_server(args, Handler)

if __name__=='__main__':
    main()
