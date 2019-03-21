

from xsqlalchemy.tables import table, column
from .base import BaseCatalog

@table("departments")
class Departments(BaseCatalog):
    level = column(int, is_require=True)
    level_code = column(str, data_len=5000)
    parent_id = column(int)


