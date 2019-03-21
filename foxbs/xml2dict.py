def __parse_node__(root):
    import sys
    ret = {}
    if not hasattr(root,"tagName"):
        return
    property_name = root.tagName
    children = [n for n in root.childNodes if hasattr(n,"tagName")]
    if hasattr(root,"attributes") and root.attributes.length>0:
        _type = root.attributes.get("type", None)
        _value = root.attributes.get("value", None)
        if _value != None:
            _value = _value.value
        if _type != None:
            _type = _type.value
        data_type = None
        if _type != None:
            if sys.version_info[0]==2:
                if not __builtins__.has_key(_type):
                    raise Exception("'{0}' is invalid data type".format(_type))
                data_type = __builtins__[_type]
            if sys.version_info[0] == 3:
                if not __builtins__.get(_type):
                    raise Exception("'{0}' is invalid data type".format(_type))
                data_type = __builtins__.get(_type)
        if data_type == list:
            lst = [__parse_node__(n) for n in children]
            ret.update({
                property_name:lst
            })
        elif data_type == None:
            ret.update({
                property_name:_value
            })
        else:
            ret.update({
                property_name: data_type(_value)
            })
    else:
        sub = {}
        for n in children:
            ret_n = __parse_node__(n)
            if ret_n != None:
                sub.update(ret_n)
        ret.update({
            property_name:sub
        })

    return ret


def load_from_file(file_path):
    from xml.dom import minidom
    nodes = minidom.parse(file_path)
    data = __parse_node__(nodes.childNodes[0])
    ret = {}
    for k,v in data.items():
        for x,y in v.items():
            ret.update({
                x:y
            })
    return ret
