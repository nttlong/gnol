class __controller_wrapper__(object):
    def __init__(self,url,template,*args,**kwargs):
        self.url = url
        self.template = template
        self.controller_class = None
        self.instance = None
        pass
    def wrapper(self,*args,**kwargs):
        # hold origin class of controller
        self.controller_class = args[0]
        # build url if it was not declare at decoration
        if not self.url:
            self.url = args[0].__module__.replace('.', '/') + '/' + args[0].__name__
        # build template if it was not declare at decoration
        if not self.template:
            self.template = self.url+".html"
        # create instance from controller declare
        self.instance = self.controller_class.__new__(self.controller_class)
        super(self.controller_class, self.instance).__init__()
        self.instance.__init__()
        pass

def controller(url = None, template= None,*args,**kwargs):
    ret = __controller_wrapper__(
        url = url,
        template = template,
        *args,
        **kwargs
    )
    return ret.wrapper