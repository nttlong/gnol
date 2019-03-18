"""

"""


def load_apps(apps_dir,flask_application):
    from . import utils
    ret_app_package = []
    list_of_app_package = utils.get_all_package_in_sub_dirs(apps_dir)
    for x in list_of_app_package:
        mdl = utils.load_app_controller(x)
    return ret_app_package



