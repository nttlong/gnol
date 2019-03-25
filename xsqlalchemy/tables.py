from itertools import islice

__tables__ = None

__sort_types__ = {
    "asc":1,
    "desc":-1
}

class ColumnInfo(object):

    def __init__(self,
                 data_type=str,
                 is_require = False,
                 is_primary = False,
                 unique_name = None,
                 is_unique = False,
                 is_auto = False,
                 data_len=None,
                 default_value = None):
        self.data_type = data_type
        self.is_require = is_require
        self.is_primary = is_primary
        self.unique_name = unique_name
        self.is_unique = is_unique
        self.is_auto = is_auto
        self.data_len =data_len
        self.default_value = default_value
        self.asc = 1
        self.desc = 1


def column(data_type=str,
           is_require = False,
           is_primary = False,
           unique_name = None,
           is_unique = False,
           is_auto = False,
           data_len = 0):
    return ColumnInfo(data_type,
                      is_require,
                      is_primary,
                      unique_name,
                      is_unique,
                      is_auto,
                      data_len)


def __find_map_types__(data_type):
    from datetime import datetime
    from sqlalchemy import  DateTime, String, Integer, Boolean, Float
    maps = [int,bool,datetime,str,float]
    sql_map = [Integer,Boolean,DateTime,String,Float]
    return sql_map[maps.index(data_type)]


def __extract_columns__(cls):
    import sys
    ret = []
    __continue__ = True

    if sys.version_info[0] == 2:
        __continue__ = cls.__bases__.__len__() > 0
    if sys.version_info[0] == 3:
        __continue__ = cls.__bases__[0] != object

    while __continue__:
        cols = [(k, v) for k, v in cls.__dict__.items() if (k.__len__()>4 and k[:2]!="__" and k[-2:]!="__") or (k.__len__()<=4)]
        ret.extend(cols)
        cls = cls.__bases__[0]
        if sys.version_info[0] == 2:
            __continue__ = cls.__bases__.__len__() > 0
        if sys.version_info[0] == 3:
            __continue__ = cls.__bases__[0] != object
    cols = [(k, v) for k, v in cls.__dict__.items() if
            (k.__len__() > 4 and k[:2] != "__" and k[-2:] != "__") or (k.__len__() <= 4)]
    ret.extend(cols)
    return ret

def table(name):
    global __tables__
    if not __tables__:
        __tables__ = {}
    if __tables__.get(name,None):
        raise Exception("{0} is already declare at ".format(name))

    def wrapper(*args,**kwargs):
        from sqlalchemy import Column,  String, ForeignKey, MetaData, Table, UniqueConstraint, Sequence
        columns = __extract_columns__(args[0])

        meta = MetaData()
        params = name, meta
        for x in columns:
            col = x[1]
            _kwargs={}
            if isinstance(col,ColumnInfo):
                data_type = __find_map_types__(col.data_type)
                if data_type == String:
                    if col.data_len:
                        data_type = data_type(col.data_len)
                if col.is_primary:
                    _kwargs.update({
                        "primary_key": True
                    })
                if col.is_require:
                    _kwargs.update({
                        "nullable": False
                    })
                else:
                    _kwargs.update({
                        "nullable": True
                    })
                if col.is_auto:
                    _kwargs.update({

                    })
                params += Column(x[0],data_type,**_kwargs),
        tbl = Table(*params)
        __tables__.update({
            name: tbl
        })
        return Fields(tbl,columns)
    return wrapper


def __get_other_value__(v):
    if isinstance(v,Field):
        return v.col
    else:
        return v

class __field_value__(object):

    def __init__(self, key, value):
        self.key = key
        self.value = value


class __Binary_Expr__(object):

    def __init__(self,left,right):
        self.left = left
        self.right = right


class Field(object):

    def __init__(self, owner, name, col):
        self.name = name
        self.col = col
        self.sort_by = None
        self.__alias__ = None
        self.__owner__= owner

    def __add__(self, other):
        self.col = self.col + __get_other_value__(other)
        return self

    def __sub__(self, other):
        self.col = self.col - __get_other_value__(other)
        return self

    def __mul__(self, other):
        self.col = self.col - __get_other_value__(other)
        return self

    def __div__(self, other):
        self.col = self.col - __get_other_value__(other)
        return self

    def __divmod__(self, other):
        self.col = self.col - __get_other_value__(other)
        return self

    def __lshift__(self, other):
        return __field_value__(self.name, other)

    def __eq__(self, other):
        self.col = self.col == __get_other_value__(other)
        if isinstance(other,Field):
            if isinstance(self.__owner__, Fields):
                self.left = self.__owner__.__sqlalchemy_table__
                self.right = other.__owner__.__sqlalchemy_table__
        return self

    def __gt__(self, other):
        self.col = self.col > __get_other_value__(other)
        return self

    def __ge__(self, other):
        self.col = self.col >= __get_other_value__(other)
        return self

    def __lt__(self, other):
        self.col = self.col < __get_other_value__(other)
        return self

    def __le__(self, other):
        self.col = self.col <= __get_other_value__(other)
        return self

    def __ne__(self, other):
        self.col = self.col != __get_other_value__(other)
        return self

    def __and__(self, other):
        from  sqlalchemy import Table
        from sqlalchemy import and_
        self.col = and_(self.col, __get_other_value__(other))
        if hasattr(self,"left"):
            self.left = __Binary_Expr__(self.left,self.right)
        if isinstance(other,Field):
            if hasattr(other,"left"):
                self.right = __Binary_Expr__(self.left,self.right)
        return self

    def __or__(self, other):
        from sqlalchemy import or_
        self.col = or_(self.col, __get_other_value__(other))
        return self

    def __neg__(self):
        from sqlalchemy import not_
        self.col = not_(self.col)
        return self

    def __getattr__(self, item):
        if __sort_types__[item]:
            self.sort_by = __sort_types__[item]
        return self

    def __rshift__(self, other):
        if isinstance(other,Field):
            self.__alias__ = other.name
        else:
            self.__alias__ = other
        self.col = self.col.label(self.__alias__)
        return self


class Fields(object):

    def __init__(self,sqlalchemy_table,cols):
        self.__sqlalchemy_table__ = sqlalchemy_table
        self.columns = cols

    def __getattr__(self, item):
        if hasattr(self.__sqlalchemy_table__.c, item):
            return Field(self, item, getattr(self.__sqlalchemy_table__.c, item))
        else:
            raise Exception("{0} was not found".format(item))



