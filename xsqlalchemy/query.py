
class qr(object):
    def __init__(self,entity):
        from .config import __connection_string__
        import sqlalchemy as db
        from sqlalchemy import Column

        self.__selected_fields__ = None
        from .tables import Fields
        if not isinstance(entity,Fields):
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
        data = args[0]
        data_insert = {}
        for k,v in data.items():
            if isinstance(k,Column):
                data_insert.update({
                    k.name:v
                })
        return self.engine.execute(self.entity.__sqlalchemy_table__.insert(),**data_insert)

    def to_list(self):
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=self.engine)
        session = Session()
