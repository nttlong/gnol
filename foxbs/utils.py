__apps__ = None

def get_app_by_path(path_to_app):
    import os
    import sys
    global __apps__
    if not __apps__:
        __apps__ = {}
    init_file_name = os.sep.join([path_to_app,"__init__.py"])
    module_name ="apps.{0}".format(
        os.path.dirname(path_to_app)
    )
    if not os.path.isfile(init_file_name):
        raise Exception("{0} was not found in {1}".format(
            "__init__.py",
            path_to_app
        ))
    import importlib
    sys.path.append(path_to_app)
    mdl = importlib.import_module(module_name)
    __apps__.update({
        module_name:mdl
    })



def get_all_sub_dirs(path_to_dir):
    import os
    return [os.sep.join([path_to_dir,x]) for x in list(os.walk(path_to_dir))[0][1] if os.path.isdir(os.sep.join([path_to_dir,x]))]


def get_all_files(path_to_dir):
    import os
    if not os.path.isdir(path_to_dir):
        raise Exception("{0} was not found".format(path_to_dir))
    return [os.sep.join([path_to_dir,x]) for x in list(
        os.walk(path_to_dir))[0][2] if os.path.isfile(os.sep.join([path_to_dir, x])
                                                      )]


def get_all_package_in_sub_dirs(path_to_dir):
    import os
    ret = get_all_sub_dirs(path_to_dir)
    return [x for x in ret if os.path.isfile(os.sep.join([x, "__init__.py"]))]


def load_app_controller(path_to_app):
    import sys
    import os
    import importlib
    ret_controllers =[]
    app_module_name = os.path.basename(path_to_app)
    app_module = importlib.import_module("apps."+app_module_name)

    controller_dir = os.sep.join([path_to_app, "controllers"])
    sys.path.append(controller_dir)
    files_in_controller_dir = [x for x in get_all_files(controller_dir) if os.path.splitext(x)[1] == ".py"]

    for x in files_in_controller_dir:
        controller_name = "apps."+app_module_name+".controllers."+os.path.splitext(os.path.basename(x))[0]

        mdl = importlib.import_module(controller_name)
        setattr(mdl,"application",app_module)
        ret_controllers.append(mdl)
        #
        # if sys.version_info[0] == 3:
        #     from importlib.machinery import SourceFileLoader
        #     mdl = SourceFileLoader(controller_name, x).load_module()
        #     ret_controllers.append(mdl)
    return ret_controllers


def load_apps(path_to_apps, flask_application):
    import os
    ret = {}
    dirs = get_all_package_in_sub_dirs(path_to_apps)
    for x in dirs:
        app_name = os.path.basename(x)
        controllers = load_app_controller(x)
        ret.update({
            app_name: controllers
        })
    return ret

def is_app_package(mdl):
    if not hasattr(mdl,"settings"):
        raise Exception("settings was not found in {0}".format(mdl))


