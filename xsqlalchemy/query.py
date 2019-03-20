
class qr(object):
    def __init__(self,entity):
        from .config import __connection_string__
        import sqlalchemy as db
        self.__selected_fields__ = None
        from .tables import Fields
        if not isinstance(entity, Fields):
            raise Exception("entity is not a table")
        self.entity=entity
        self.engine = db.create_engine(__connection_string__)

    def select(self,*args,**kwargs):
        self.__selected_fields__ = list(args)
        return self

    def insert(self,*args,**kwargs):
        from sqlalchemy import insert,Column
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=self.engine)
        session = Session()
        data = args
        data_insert = args[0]
        if not isinstance(data_insert,dict):
            for field in data:
                data_insert.update({
                    field['field_name']: field['value']
                })

        return self.engine.execute(self.entity.__sqlalchemy_table__.insert(), **data_insert)

    def where(self,*args,**kwargs):
        return self

    def to_list(self):
        from sqlalchemy.orm import sessionmaker
        tmp_dict = {}
        _session = sessionmaker(bind=self.engine)
        session = _session()
        selected_fields = ()
        for x in self.__selected_fields__:
            tmp_dict.update({x.name: None})
            field = getattr(self.entity.__sqlalchemy_table__.c, x.name)
            selected_fields += (field,)
        lst = session.query(*selected_fields).all()
        for item in lst:
            dic = tmp_dict.copy()
            y=0
            for k,v in dic.items():
                dic[k]= item[y]
                y = y + 1
            yield dic



