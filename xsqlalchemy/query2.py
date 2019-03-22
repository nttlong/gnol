
class Queryable(object):
    def __init__(self,*args):
        import sqlalchemy as db
        from .config import __connection_string__
        self.__query__ = None
        self.__header__ = []
        self.__select__ = []
        for x in args:
            self.__select__.append(x.col)
            if x.__alias__:
                self.__header__.append(x.__alias__)
            else:
                if self.__header__.count(x.col.name)==0:
                    self.__header__.append(x.col.name)
                else:
                    self.__header__.append(x.col.table.name+"_"+x.col.name)

        self.__tables__ = list(set([x.__owner__.__sqlalchemy_table__ for x in args]))
        self.engine = db.create_engine(__connection_string__)
        from sqlalchemy.orm import sessionmaker
        _session = sessionmaker(bind=self.engine)
        session = _session()
        self.__query__ = session.query(*self.__select__)

    def __repr__(self):
        return self.__query__.__str__()

    def __str__(self):
        return self.__query__.__str__()

    def join(self,expr):
        from sqlalchemy import Table
        right_table = expr.right
        while not isinstance(right_table,Table):
            right_table = right_table.right
        self.__query__ = self.__query__.join(right_table, expr.col)
        return self
    def outer_join(self,expr):
        from sqlalchemy import Table
        right_table = expr.right
        while not isinstance(right_table,Table):
            right_table = right_table.right
        self.__query__ = self.__query__.outerjoin(right_table, expr.col)
        return self

    def where(self,expr):
        self.__query__= self.__query__.filter(expr.col)
        return self

def select(*args):
    return Queryable(*args)