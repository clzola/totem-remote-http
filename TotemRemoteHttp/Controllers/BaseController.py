from urllib.parse import urlparse, parse_qs

class BaseController:
    def __init__(self, server, request):
        self.__server = server
        self.__request = request
        self.__query = parse_qs(urlparse(request.path).query)
        
    @property
    def server(self):
        return self.__server
        
    @property
    def request(self):
        return self.__request
        
    @property
    def query(self):
        return self.__query
