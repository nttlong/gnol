

class __data__(object):
    def __init__(self, data):
        self.__dict__.update(data)


class qr(object):


    def __init__(self,entity):
        from .config import __connection_string__
        import sqlalchemy as db
        self.__selected_fields__ = None
        self.__where__ = None
        from .tables import Fields
        if not isinstance(entity, Fields):
            raise Exception("entity is not a table")
        self.entity=entity
        self.engine = db.create_engine(__connection_string__)
        self.__limit__ = None
        self.__offset__ = None
        self.__sort__ = None
        self.__query_set__ = None

    def select(self,*args,**kwargs):
        self.__selected_fields__ = list(args)
        return self

    def insert(self, *args, **kwargs):
        try:
            from sqlalchemy import insert,Column
            from sqlalchemy.orm import sessionmaker
            Session = sessionmaker(bind=self.engine)
            session = Session()
            data = args
            data_insert = args[0]
            if not isinstance(data_insert, dict):
                data_insert = {}
                for field in data:
                    data_insert.update({
                        field.key: field.value
                    })

            ret_insert = self.engine.execute(self.entity.__sqlalchemy_table__.insert(), **data_insert)
            ret_data = __data__(data_insert)
            ret_data.id = ret_insert.inserted_primary_key[0]
            return ret_data, None
        except Exception as ex:
            return None, ex

    def where(self,*args,**kwargs):
        self.__where__ = args[0]
        return self

    def __build_query__(self):
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.sql.selectable import Join
        from sqlalchemy import desc, asc
        header = []
        _session = sessionmaker(bind=self.engine)
        session = _session()
        selected_fields = ()
        header_index = 0
        _qr = None
        if self.__selected_fields__:
            for x in self.__selected_fields__:
                header_item = dict(
                    field=x.name,
                    index=header_index
                )
                if x.__alias__:
                    header_item["field"] = x.__alias__
                header.append(header_item)

                field = x.col
                if x.__alias__:
                    field = field.label(x.__alias__)
                selected_fields += (field,)
                header_index = header_index + 1
            _qr = session.query(*selected_fields)
            if isinstance(self.__query_set__,Join):
                _qr = _qr.select_from(self.__query_set__)

        else:
            for x in self.entity.columns:
                header.append(dict(
                    field=x[0],
                    index=header_index
                ))
                field = getattr(self.entity.__sqlalchemy_table__.c, x[0])
                selected_fields += (field,)
                header_index = header_index + 1
            _qr = session.query(*selected_fields)
            if isinstance(self.__query_set__, Join):
                _qr = _qr.select_from(self.__query_set__)
        if self.__sort__:
            for x in self.__sort__:
                if x["sort_by"] == 1:
                    _qr = _qr.order_by(asc(getattr(self.entity.__sqlalchemy_table__.c, x["field"])))
                else:
                    _qr = _qr.order_by(desc(getattr(self.entity.__sqlalchemy_table__.c, x["field"])))
        if self.__where__:
            _qr = _qr.filter(self.__where__.col)
        if self.__sort__:
            _qr = _qr
        if self.__limit__:
            _qr._limit = self.__limit__
        if self.__offset__:
            _qr._offset = self.__offset__
        return header, _qr

    def all(self):
        header, _qr = self.__bulid_query__()
        return header, _qr.all()

    def limit(self, num):
        self.__limit__ = num
        return self

    def offset(self,num):
        self.__offset__ = num
        return self

    def to_pandas_data_frame(self):
        from pandas import DataFrame
        header, items = self.all()
        df = DataFrame(items, columns=[k["field"] for k in header])
        return df

    def to_list(self):
        tmp_dict = {}
        header, data  = self.all()

        for x in header:
            tmp_dict.update({
                x["field"]: x["index"]
            })

        for item in data:
            dic = tmp_dict.copy()
            y=0
            for k,v in dic.items():
                dic[k]= item[v]
                y = y + 1
            yield dic

    def update(self, *args):
        try:
            data = args
            data_update = args[0]
            if not isinstance(data_update, dict):
                data_update = {}
                for field in data:
                    data_update.update({
                        field.key: field.value
                    })
            ret_update = self.engine.execute(self.entity.__sqlalchemy_table__.update(self.__where__.col), **data_update)
            return ret_update, None
        except Exception as ex:
            return None, ex

    def sort(self,*args):
        if not self.__sort__:
            self.__sort__ = []
        for x in args:
            self.__sort__.append(dict(
                field = x.name,
                sort_by = x.sort_by
            ))
        return self

    def join(self, entity, expr):
        from sqlalchemy.sql import Join
        if isinstance(self.__query_set__, Join):
            self.__query_set__ = self.__query_set__.join(entity.__sqlalchemy_table__, expr.col)
        else:
            self.__query_set__= self.entity.__sqlalchemy_table__.join(entity.__sqlalchemy_table__, expr.col)
        return self

    def outer_join(self, entity, expr):
        from sqlalchemy.sql import Join
        if isinstance(self.__query_set__, Join):
            self.__query_set__ = self.__query_set__.outerjoin(entity.__sqlalchemy_table__, expr.col)
        else:
            self.__query_set__= self.entity.__sqlalchemy_table__.outerjoin(entity.__sqlalchemy_table__, expr.col)
        return self

    def to_sql_command(self):
        from sqlalchemy.dialects import postgresql

        h,_qr = self.__build_query__()
        return _qr.__str__()
    def __repr__(self):
        h, _qr = self.__build_query__()
        return _qr.__str__()

