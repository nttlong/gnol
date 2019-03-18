class Server(object):
    def __init__(self):
        self.request = None
    def to_json(self):
        return 1


class BaseModel(object):
    def __init__(self,app_module):
        from flask import request
        self.server = Server
        self.server.request = request
        self.server.root_url = request.url_root.rstrip("/")
        if app_module.host_dir:
            self.server.static = self.server.root_url+"/"+app_module.host_dir+"/static"
        else:
            self.server.static = self.server.root_url + "/static"
        def to_json():
            return 1




