import foxbs
from apps.ui.controllers.commons import test001

@foxbs.controller(
    url="",
    template="index.html"
)
class IndexController(test001):
    def __init__(self):
        x= self.application
        pass
    def on_get(self,model):
        return self.render(model)
