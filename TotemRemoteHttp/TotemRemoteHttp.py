from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from gi.repository import GObject, Peas, Totem, Gtk, Gio;
from threading import Thread
from urllib.parse import urlparse
import re, os

from Controllers.BaseController import BaseController
from Controllers.InterfaceController import InterfaceController
from Controllers.PlayerController import PlayerController


class TotemRemoteHttp(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'TotemRemoteHttp'
    object = GObject.Property (type = GObject.Object)
    
    def __init__(self):
        GObject.Object.__init__ (self)
        self.server_address = ('', 9090)
        self.server = None
        self.server_thread = None
        self.window = None
        self.totem = None
        
    def do_activate (self):
        print('Activating TotemRemoteHttp plugin')
        self.totem = self.object
        
        #action = Gio.SimpleAction.new('totem-remote-http', None)
        #action.connect('activate', self._show_window)
        #self.totem.add_action(action)
        #self._show_window()
        
        if self.server == None:
            self.server = TotemRemoteHttpServer(self.server_address, self.totem)
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
    def do_deactivate (self):
        print('Deactivating TotemRemoteHttp plugin')
        self.server.shutdown()
        if self.window is not None:
            self.window.destroy()
            self.window = None
        
    def _show_window(self):
        self.window = Gtk.Window()
        self.window.set_title('TotemRemoteHttp Settings')
        self.window.connect('destroy', self._destroy_window)
        
        self.window.set_default_size(300, 300)
        
        port_label = Gtk.Label()
        port_label.set_text("Port")
        self.window.add(port_label)
        
        port_input = Gtk.Entry()
        port_input.set_width_chars(10)
        self.window.add(port_input)
        
        self.window.show_all()
    
    def _destroy_window(self, *args):
        self.window.destroy()
        self.window = None
 
        
class TotemRemoteHttpServer(HTTPServer):
     def __init__(self, server_addr, player):
        HTTPServer.__init__(self, server_addr, TotemRemoteHttpRequestHandler)
        self.player = player
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        
 
class TotemRemoteHttpRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        routes = [
            {'regexp': r'^/$', 'controller': 'InterfaceController', 'action': 'actionIndex'},
            {'regexp': r'^/interface$', 'controller': 'InterfaceController', 'action': 'actionIndex'},
            {'regexp': r'^/hello$', 'controller': 'InterfaceController', 'action': 'actionHello'},
            {'regexp': r'^/status$', 'controller': 'PlayerController', 'action': 'actionStatus'},
            {'regexp': r'^/volume/([0-9\.]+)$', 'controller': 'PlayerController', 'action': 'actionVolume'},
            {'regexp': r'^/forward$', 'controller': 'PlayerController', 'action': 'actionForward'},
            {'regexp': r'^/backward$', 'controller': 'PlayerController', 'action': 'actionBackward'},
            {'regexp': r'^/seek/([0-9]+)$', 'controller': 'PlayerController', 'action': 'actionSeek'},
            {'regexp': r'^/toggle/fullscreen$', 'controller': 'PlayerController', 'action': 'actionToggleFullscreen'},
            {'regexp': r'^/playlist/next$', 'controller': 'PlayerController', 'action': 'actionNext'},
            {'regexp': r'^/playlist/previous$', 'controller': 'PlayerController', 'action': 'actionPrevious'},
            {'regexp': r'^/playpause$', 'controller': 'PlayerController', 'action': 'actionPlayPause'},
            {'regexp': r'^/remote/([A-Z_]+)$', 'controller': 'PlayerController', 'action': 'actionRemote'},
            {'regexp': r'^/hash$', 'controller': 'PlayerController', 'action': 'actionHash'},
        ]
        
        self.__router = Router(server, self)
        for route in routes:
            self.__router.addRoute(route['regexp'], route['controller'], route['action'])
            
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):            
        request_components = urlparse(self.path)
        if self.__router.route(request_components.path) == True:
            return
            
        SimpleHTTPRequestHandler.do_GET(self)
        
        
    def do_POST(self):
        request_components = urlparse(self.path)
        if self.__router.route(request_components.path) == True:
            return
            
        self.send_response(404, 'Route Not Found')
        self.end_headers()


class Router:
    def __init__(self, server, request):
        self.__routes = []
        self.__server = server
        self.__request = request
        
    def addRoute(self, regexp, controller, action):
        self.__routes.append({'regexp': regexp, 'controller': controller, 'action': action})
        
    def route(self, path):
        for route in self.__routes:
            match = re.search(route['regexp'], path)
            if match:
                cls = globals()[route['controller']]
                func = cls.__dict__[route['action']]
                obj = cls(self.__server, self.__request)
                func(obj, *match.groups())
                return True

        # Not found
        #self.__request.send_response(404, 'Route Not Found')
        #self.__request.end_headers()
        return False

