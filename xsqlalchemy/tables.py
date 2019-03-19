__tables__ = None


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
    ret = []
    while cls.__bases__[0] != object:
        cols = [(k, v) for k, v in cls.__dict__.items() if (k.__len__()>4 and k[:2]!="__" and k[-2:]!="__") or (k.__len__()<=4)]
        ret.extend(cols)
        cls = cls.__bases__[0]
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
        return Fields(tbl)
    return wrapper


class Field(object):
    def __init__(self,name):
        self.name=name
    def __lshift__(self, other):
        return dict(field_name=self.name,value=other)


class Fields(object):
    def __init__(self,sqlalchemy_table):
        self.__sqlalchemy_table__ = sqlalchemy_table
    def __getattr__(self, item):
        return getattr(self.__sqlalchemy_table__.columns,item)

