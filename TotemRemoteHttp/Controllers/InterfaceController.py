from Controllers.BaseController import BaseController
import os

class InterfaceController(BaseController):
    def __init__(self, server, request):
        BaseController.__init__(self, server, request)
        self.__player = self.server.player
        
    def actionIndex(self):
        with open('interface.html', 'r') as interface_file:
            html = interface_file.read()
            
        self.request.send_response(200)
        self.request.send_header('Content-type', 'text/html')
        self.request.end_headers()
        self.request.wfile.write(bytes(html, 'UTF-8'))
        
    def actionApi(self):
        with open('api.html', 'r') as interface_file:
            html = interface_file.read()
            
        self.request.send_response(200)
        self.request.send_header('Content-type', 'text/html')
        self.request.end_headers()
        self.request.wfile.write(bytes(html, 'UTF-8'))
   
    def actionHello(self):
        self.request.send_response(200)
        self.request.send_header('Content-type', 'text/html')
        self.request.end_headers()
        self.request.wfile.write(bytes('Hello World', 'UTF-8'))

