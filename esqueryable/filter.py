class Fields(object):
    def __init__(self,name=None):
        self.__name__ = name
        self.__expr__ = None



    def __getattr__(self, item):
        if self.__name__:
            return Fields(self.__name__+"."+ item)
        else:
            return Fields(item)

    def __lshift__(self, other):
        self.__expr__ = {
            "match": {
                self.__name__: {
                    "query": other
                }
            }
        }
        return self

    def __eq__(self, other):
        self.__expr__ = {
            "match": {
                self.__name__: {
                    'query':other,
                    "type": "phrase"
                }
            }
        }
        return self

    def __gt__(self, other):
        self.__expr__ = {
            "range": {
                self.__name__: {
                    "gt": other
                }
            }
        }
        return self

    def __ge__(self, other):
        self.__expr__ = {
            "range": {
                self.__name__: {
                    "from": other
                }
            }
        }
        return self

    def __lt__(self, other):
        self.__expr__ = {
            "range": {
                self.__name__: {
                    "lt": other
                }
            }
        }
        return self

    def __le__(self, other):
        self.__expr__ = {
            "range": {
                self.__name__: {
                    "to": other
                }
            }
        }

        return self

    def __and__(self, other):
        if not isinstance(other,Fields):
            raise Exception("Can not and with {0}",type(other))
        _expr_ = {
            "bool":{
                "must":[
                    self.__expr__, other.__expr__
                ]
            }
        }

        self.__expr__ = _expr_

        return self

    def __or__(self, other):
        if not isinstance(other,Fields):
            raise Exception("Can not and with {0}",type(other))
        _expr_ = {
            "bool":{
                "should":[
                    self.__expr__, other.__expr__
                ]
            }
        }
        self.__expr__ = _expr_
        return self

    def __ne__(self, other):
        _expr_ = {
            "bool": {
                "must_not" :{
                    "match" : {
                        self.__name__: {
                            'query': other,
                            "type": "phrase"
                        }
                    }
                }
            }
        }
        self.__expr__ = _expr_
        return self







# def search_all(value = None,fields=None,page_size=50,page_index=0):
#     _fields = []
#     _from = page_index*page_size
#     size = page_size
#     if isinstance(fields,list):
#         for x in fields:
#             if isinstance(x,Fields):
#                 _fields.append(x.__name__)
#     if isinstance(fields,Fields):
#         _fields.append(fields.__name__)
#
#
#     if not value:
#         return {
#             "from": _from,
#             "size":size,
#             "query": {
#                 "match_all": {}
#             }
#         }
#     elif _fields.__len__()>0:
#         _match = []
#         for f in _fields:
#
#             _match.append({
#                 "match":{
#                     f: {
#                         "query": value
#                     }
#                 }
#             })
#         return {
#             "from": _from,
#             "size": size,
#             "query": {
#                 "bool":{
#                     "must":_match
#                 }
#             }
#         }
#
#     else:
#         return {
#             "from": _from,
#             "size": size,
#             "query":{
#                 "match":{
#                     "_all":{
#                         "query":value,
#                         "type": "phrase"
#                     },
#
#                 }
#             }
#         }
# ,
#                     "type": "phrase"
#
# def where(search):
#     ret ={}
#     if isinstance(search,dict):
#         ret.update({
#             "from":search["from"],
#             "size":search["size"],
#             "query":{
#                 "bool":{
#                     "must":[
#                         {"match":search["query"].get("multi_match",search["query"].get("match"))}
#                     ]
#                 }
#             }
#         })
#         # search['query'].update({
#         #     "constant_score":{
#         #     "filter":{
#         #     "bool":{
#         #         "should":{
#         #             "term":{
#         #                 "course_info.org":"lv"
#         #             }
#         #         }
#         #     }}
#         # }})
#     return ret
#

def get_elasticsearch_filter(fields):
    if isinstance(fields,Fields):
        return {"query" : fields.__expr__}