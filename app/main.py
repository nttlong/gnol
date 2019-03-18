import sys
import os
import foxbs
ROOT_REPO = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_REPO)


app = foxbs.create_flask_app(__name__, os.sep.join([ROOT_REPO, "apps"]))



# @app.route("/")
# def hello():
#     return "Hello World! version {0}".format("XXX")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
