from xsqlalchemy.tables import column
from datetime import datetime


class BaseTable:

    id = column(int, is_primary=True)
    description = column(str,data_len=2000)
    created_on = column(datetime, is_require=True)
    created_by = column(str, data_len=60)
    modified_on = column(datetime)
    modified_by = column(str, data_len=60)


class BaseCatalog(BaseTable):

    code = column(str,data_len= 50,is_unique=True)
    name = column(str,data_len = 200)
    fname = column(str,data_len= 200)

