

from . import config
from . query import qr
from .tables import table, column
from .index import create_index


def engine():
    import sqlalchemy as db
    return db.create_engine(config.__connection_string__)


def create_all():
    from . import tables
    from sqlalchemy import Index, UniqueConstraint
    from xsqlalchemy.index import __index_cache__
    for k,v in tables.__tables__.items():
        v.create(engine(),True)
    for k,v in __index_cache__.items():
        tb_index= Index(k,unique=v["is_unique"], _table=v["table"],*v["columns"])
        try:
            tb_index.create(bind=engine())
        except Exception as ex:
            print (ex.message)



