class __controller_wrapper__(object):
    def __init__(self,url,template,*args,**kwargs):
        self.url = url
        self.template = template
        self.controller_class = None
        self.instance = None
        pass

    def wrapper(self,*args,**kwargs):
        import foxbs
        import sys
        import os
        inherist = []
        from . base_controller import BaseController
        # hold origin class of controller
        self.controller_class = args[0]
        app_module_name = self.controller_class.__module__.split(".controllers.")[0]
        app_module = sys.modules[app_module_name]
        if not hasattr(app_module,"host_dir"):
            raise Exception("host_dir was not found in {0}".format(app_module.__file__))
        if not hasattr(app_module, "static_dir"):
            setattr(app_module,"static_dir",os.sep.join([foxbs.REPO_ROOT,app_module_name.replace(".", os.sep),"static"]))
        if not issubclass(self.controller_class,BaseController):
            raise Exception("{0} is not inherit from {1}".format(
                self.controller_class, BaseController
            ))
        # build url if it was not declare at decoration
        if self.url == None:
            self.url = app_module_name.replace("apps.","").replace(".","/") + '/' + args[0].__name__
        # build template if it was not declare at decoration
        if not self.template:
            self.template = self.url+".html"
        cls = self.controller_class
        is_match_object = False
        while not cls.__bases__[0] is BaseController:
            if cls is object:
                is_match_object = True
                break
            inherist.append(cls.__bases__[0])
            cls = cls.__bases__[0]
        if is_match_object:
            raise Exception

        # create instance from controller declare
        self.instance = self.controller_class.__new__(self.controller_class)
        setattr(self.instance,"application", app_module)
        while inherist.__len__()>0:
            tmp_cls = inherist.pop()
            super(tmp_cls, self.instance).__init__()
        super(self.controller_class, self.instance).__init__()
        if hasattr(self.instance,"__init__"):
            self.instance.__init__()
        self.instance.template_path = os.sep.join([app_module_name.replace(".",os.sep),"templates",self.template])

        def handler():
            from flask import request
            from flask import make_response
            from flask import session
            from flask_wtf import csrf

            from . base_model import BaseModel, __load_request_form__

            model = BaseModel(self.instance.application)
            model.server.response = make_response()
            if not session.get("csrftoken"):
                session["csrftoken"] = csrf.generate_csrf()
            model.server.csrf = session["csrftoken"]



            if request.method == "GET":
                return getattr(self.instance,"on_get")(model)
            if request.method == "POST":
                if request.headers['Ajax-Post']:
                    from .json_convert import json_serial, to_json, from_json
                    __load_request_form__(model.client_post, from_json(request.data))
                    method = getattr(self.instance, request.headers['Ajax-Post'])
                    return method(model)
                else:
                    __load_request_form__(model.client_post, request.form)
                    return getattr(self.instance,"on_post")(model)
            if request.method == "PUT":
                return getattr(self.instance,"on_put")(model)
            if request.method == "DELETE":
                return getattr(self.instance,"on_delete")(model)
            if request.method == "PACTH":
                return getattr(self.instance,"on_patch")(model)
        handler.__name__ = self.controller_class.__module__.replace(".", "_")

        if self.instance.application.host_dir == None:
            foxbs.flask_application.add_url_rule("/" + self.url,handler.__name__,handler,methods=['GET','POST','PUT','DELETE','PACTH'])

        else:
            foxbs.flask_application.add_url_rule("/"+ self.instance.application.host_dir+"/" + self.url, handler.__name__,handler, methods=['GET', 'POST'])

        if not hasattr(app_module,"__static_serve__"):
            def static_serve(path):
                from flask import send_from_directory
                return send_from_directory(app_module.static_dir, path)

                # return foxbs.flask_application.send_static_file(path)
            static_serve.__name__ = "__"+app_module_name.replace(".", "_")+"_static__"
            setattr(app_module,"__static_serve__", static_serve)
            if self.instance.application.host_dir == None:
                foxbs.flask_application.add_url_rule("/static/<path:path>",static_serve.__name__, static_serve, methods=['GET'])
            else:
                foxbs.flask_application.add_url_rule("/" + self.instance.application.host_dir + "/static/<path:path>",static_serve.__name__, static_serve,methods=['GET'])

            x=1
        if issubclass(type(self.instance),BaseController):
            from mako.lookup import TemplateLookup
            self.instance.host_dir = self.instance.application.host_dir
            self.instance.app_name = self.instance.application.__name__.lstrip("apps.")
            self.instance.template_dir = os.sep.join([os.path.dirname(self.instance.application.__file__), "templates"])
            self.instance.rel_template_file = self.template
            self.instance.full_path_template_file = os.sep.join([self.instance.template_dir, self.instance.rel_template_file])
            self.instance.mako_lookup = TemplateLookup(directories=[self.instance.template_dir], module_directory='/tmp/mako_modules')



def controller(url = None, template= None,*args,**kwargs):
    ret = __controller_wrapper__(
        url = url,
        template = template,
        *args,
        **kwargs
    )
    return ret.wrapper
