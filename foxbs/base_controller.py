class BaseController(object):
    application = None

    def __init__(self):
        pass

    def render(self,model):
        from flask import render_template
        return render_template(self.template_path, **model.__dict__)




