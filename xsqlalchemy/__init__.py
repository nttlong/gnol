

from . import config
from . query import qr


def engine():
    import sqlalchemy as db
    return db.create_engine(config.__connection_string__)
def create_all():
    from . import tables
    for k,v in tables.__tables__.items():
        v.create(engine(),True)


