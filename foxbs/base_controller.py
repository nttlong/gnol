class BaseController(object):
    application = None

    def __init__(self):
        self.host_dir = None
        self.app_name = None
        self.template_dir = None
        self.rel_template_file = None
        self.full_path_template_file = None
        self.mako_lookup = None

    def render(self,model):
        mytemplate = self.mako_lookup.get_template(self.rel_template_file)
        return mytemplate.render(**model.__dict__)

    def to_json(self, data):
        from .json_convert import to_json
        return to_json(data)




