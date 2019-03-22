__index_cache__ = None

def create_index(entity,is_unique=False,*args):
    from .tables import Fields, Field
    from sqlalchemy import Table
    global __index_cache__
    if not __index_cache__:
        __index_cache__ = {}
    index_name ="IX_"
    cols = ()
    if isinstance(entity,Fields):
        if isinstance(entity.__sqlalchemy_table__,Table):
            full_table_name=entity.__sqlalchemy_table__.name
            if entity.__sqlalchemy_table__.schema:
                full_table_name = entity.__sqlalchemy_table__.schema+"."+full_table_name
            index_name += full_table_name.replace(".","_")
            for x in args:
                if isinstance(x,Field):
                    index_name = index_name+"_"+x.name
                    cols+=(getattr(entity.__sqlalchemy_table__.c,x.name),)
        __index_cache__.update({
            index_name: dict(
                columns=cols,
                is_unique=is_unique,
                table=entity.__sqlalchemy_table__
            )
        })






    from sqlalchemy import Index as sqlIndex
    pass
