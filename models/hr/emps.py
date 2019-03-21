from xsqlalchemy.tables import table, column
from . base import BaseTable


@table("employees")
class Employees(BaseTable):
    id = column(data_type=int, is_primary=True)
    code = column(data_len=60, is_unique=True, is_require=True)
    first_name = column(data_len=200, is_require=True)
    last_name = column(data_len=200, is_require= True)
    department_id = column(data_type=int, is_require=True)
