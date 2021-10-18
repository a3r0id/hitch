from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
from uuid import uuid1
from threading import Thread
from json import dumps

from hitch.macros import Macros

# Server Instance
class HitchHttpServer(object):

    def __str__ (self):
        return dumps(dict(
            port=self.port,
            adapter=self.adapter,
            https=self.https
        ), default=str, indent=4)

    def __init__(
        self,
        https=False,
        content="<h1>Welcome To HitchServer!</h1>",
        content_type='text/html',
        port=80, 
        adapter="127.0.0.1", 
        ssl_cert='localhost.pem',
        requestHandler=None):

        self.port     = port
        self.port_str = str(self.port)
        self.adapter  = adapter
        self.content  = content
        self.https    = https
        self.content_type = content_type
        self.ssl_cert = ssl_cert

        # overrides SimpleHTTPRequestHandler with a custom get handler and removes other HTTP verb handlers.
        class Handler(SimpleHTTPRequestHandler):

            #override
            def do_GET(self):

                self.content = content
                self.content_type = content_type

                # For dynamic usage-cases like serving custom javascript/images etc and interacting with path etc.
                if requestHandler is not None:
                    # See utils.py -> exampleHTTPRequestHandler :)
                    requestHandler(self)

                else:
                    # Just serves one document, allows setting content type and content but path is ignored.
                    self.send_response(200)
                    self.send_header('Content-type', self.content_type)
                    self.end_headers()
                    self.wfile.write(bytes(self.content, "utf-8"))

                return None

            #override
            def do_POST(self):
                return None
                
            #override 
            def do_HEAD(self):
                return None

        self.server = HTTPServer((self.adapter, self.port), Handler)
        h = "http://"
        
        if https:
            h = h.replace('tp', 'tps')
            self.server.socket = ssl.wrap_socket(self.server.socket,
                                        server_side=True,
                                        certfile=self.ssl_cert,
                                        ssl_version=ssl.PROTOCOL_TLS)

        # Store server instance globally
        Macros.http_servers[self.port_str] = self

        def parallel_thread(self):
            self.server.serve_forever()
        
        self.thread = Thread(target=parallel_thread, args=(self,))
        self.thread.start()
        
        print(f"Started New Thread. Starting HTTP/S Server @ {h}{self.adapter}:{self.port}...")

