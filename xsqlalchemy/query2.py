
class Queryable(object):

    def __init__(self,*args):
        import sqlalchemy as db
        from sqlalchemy.orm.query import Query
        if isinstance(args[0],Query):
            self.__query__ =args[0]
            return
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
        ret = Queryable(self.__query__.join(right_table, expr.col))
        return ret

    def outer_join(self,expr):
        from sqlalchemy import Table
        right_table = expr.right
        while not isinstance(right_table,Table):
            right_table = right_table.right
        ret = Queryable(self.__query__.outerjoin(right_table, expr.col))
        return ret

    def where(self,expr):
        ret = Queryable(self.__query__.filter(expr.col))
        return ret

    def union(self, *args):
        ret = args[0].__query__
        for i in range(1, args.__len__(), 1):
            ret = ret.union(args[i].__query__)
        return Queryable(ret)

    def group_by(self,*args):
        cols = ()
        for x in args:
            cols+=(x.col,)
        return Queryable(self.__query__.group_by(*cols))

    def order_by(self,*args):
        sort = ()
        for x in args:
            if x.sort_by == -1:
                sort +=(x.col.desc(),)
            else:
                sort += (x.col.asc(),)
        return Queryable(self.__query__.order_by(*sort))




def select(*args):
    return Queryable(*args)

def union(*args):
    ret = args[0].__query__
    for i in range(1,args.__len__(),1):
        ret = ret.union(args[i].__query__)
    return Queryable(ret)

def union_all(*args):
    ret = args[0].__query__
    for i in range(1,args.__len__(),1):
        ret = ret.union_all(args[i].__query__)
    return Queryable(ret)