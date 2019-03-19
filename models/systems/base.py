from xsqlalchemy.tables import table, column
import datetime


class BaseTable:
    id = column(int, is_primary=True)
    created_on = column(datetime.datetime, is_require=True)
    created_by = column(str, data_len=60)
    modified_on = column(datetime.datetime)
    modified_by = column(str, data_len=60)