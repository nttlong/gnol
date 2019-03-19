

def __load_request_form__(obj,data):
    from flask import request
    for k, v in data.items():
        obj.__dict__.update({
            k:v
        })


class Server(object):
    def __init__(self):
        self.request = None

    def to_json(self,data):
        import json
        return json.dumps(data)

    def get_language_code(self):
        from flask import session
        return session.get("language","en")

    def set_language_code(self, value):
        from flask import session
        session["language"] = value

    def csrf_token(self):
        return self.csrf
class ClientPost(object):
    def __init__(self):
        self.__dict__ = {}

class BaseModel(object):
    def __init__(self,app_module):
        from flask import request, session

        self.server = Server()
        self.server.request = request
        self.server.root_url = request.url_root.rstrip("/")
        self.server.session = session
        self.client_post = ClientPost()
        if app_module.host_dir:
            self.server.static = self.server.root_url+"/"+app_module.host_dir+"/static"
        else:
            self.server.static = self.server.root_url + "/static"





