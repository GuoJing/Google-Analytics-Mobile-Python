#!/usr/bin/env python
# encoding: utf-8

import sys
from wsgiref import simple_server
from ga import track_page_view

class application():
    def __init__(self):
        pass

    def run(self, environ, start_response):
        response = track_page_view(environ)
        start_response(response['response_code'], response['response_headers'])
        ret = response.get('response_body')
        return [ret]

if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) >= 2 else '9090'
    host = sys.argv[2] if len(sys.argv) >=3 else '127.0.0.1'
    try:
        app = application()
        print "Server Started %s:%s" % (host, port)
        httpd = simple_server.WSGIServer((host, int(port)),
            simple_server.WSGIRequestHandler)
        httpd.set_app(app.run)
        httpd.serve_forever() 
    except:
        print "Error happend"
        pass
