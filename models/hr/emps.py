from xsqlalchemy import table, column, create_index
from . base import BaseTable
from datetime import datetime


@table("employees")
class Employees(BaseTable):
    id = column(data_type=int, is_primary=True)
    code = column(data_len=60, is_unique=True, is_require=True)
    first_name = column(data_len=200, is_require=True)
    last_name = column(data_len=200, is_require= True)
    department_id = column(data_type=int, is_require=True)
    email = column(data_len=100)
    birthdate = column(data_type=datetime)


create_index(Employees,True,Employees.code)
create_index(Employees,True,Employees.email)

