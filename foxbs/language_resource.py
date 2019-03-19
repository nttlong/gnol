__language_cache__ = None
import threading
def get_language_reource_item(
        get_laguage_resource_function,
        language_code,
        app_name,
        view_path,
        key,
        value = None
):
    global __language_cache__
    if not __language_cache__:
        __language_cache__ = {}
    if not value:
        value = key

    key = key.rstrip(" ").lstrip(" ").lower()
    value = value.rstrip(" ").lstrip(" ")
    ret = __language_cache__.get(language_code,{}).get(app_name,{}).get(view_path,{}).get(key,None)
    if not ret:
        lock = threading.Lock()
        lock.acquire()
        try:
            if not __language_cache__.has_key(language_code):
                __language_cache__.update({
                    app_name: {}
                })
            if not __language_cache__[language_code]. has_key(app_name):
                __language_cache__[language_code].update({
                    app_name: {}
                })
            if not __language_cache__[language_code][app_name].has_key(view_path):
                __language_cache__[language_code][app_name].update({
                    view_path: {}
                })
            ret = get_laguage_resource_function(
                language_code,
                app_name,
                view_path,
                key,
                value
            )
            __language_cache__[language_code][app_name][view_path].update({
                key: ret
            })

            lock.release()
            return ret
        except Exception as ex:
            lock.release()
            raise ex
    else:
        return ret


