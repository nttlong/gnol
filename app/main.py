import sys
import os
ROOT_REPO = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_REPO)
import foxbs

app = foxbs.create_flask_app(__name__)
@foxbs.controller()
class Test(object):
    def on_get(self):
        pass
@app.route("/")
def hello():
    return "Hello World! version {0}"


if __name__ == "__main__":

    app.run(debug=True, use_reloader=True)