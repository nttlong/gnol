# import sqlalchemy as db
# from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, MetaData, Table
# from sqlalchemy.orm import sessionmaker
#
# engine = db.create_engine('postgres://postgres:123456@172.16.7.67:5433/fx')
# connection = engine.connect()
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
# meta = MetaData()
#
# employees = Table('employees', meta,
#     Column('employee_id', Integer, primary_key=True),
#     Column('employee_name', String(60), nullable=False, key='name')
#
# )
# Session = sessionmaker(bind = engine)
# conn = engine.connect()
# session = Session(bind=conn)
#
# employees.extend_existing(engine)

from models.systems.users import Users
fx= Users
c =fx.id