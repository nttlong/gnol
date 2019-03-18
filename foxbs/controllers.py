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
        app_module_name =  self.controller_class.__module__.split(".controllers.")[0]
        app_module = sys.modules[app_module_name]
        if not hasattr(app_module,"host_dir"):
            raise Exception("host_dir was not found in {0}".format(app_module.__file__))

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
            from . base_model import BaseModel
            model = BaseModel()
            return getattr(self.instance,"on_get")(model)
        handler.__name__ = app_module_name.replace(".", "_")+"_"+self.controller_class.__name__

        if self.instance.application.host_dir == None:
            foxbs.flask_application.route("/" + self.url)(handler)
        else:
            foxbs.flask_application.route("/"+ self.instance.application.host_dir+"/" + self.url)(handler)



def controller(url = None, template= None,*args,**kwargs):
    ret = __controller_wrapper__(
        url = url,
        template = template,
        *args,
        **kwargs
    )
    return ret.wrapper