from xsqlalchemy.tables import table, column
import datetime
from . base import BaseTable
@table("users")
class Users(BaseTable):
    username = column(data_len=60, is_require=True,is_unique=True)
    email = column(is_unique=True)
    hash_password = column()
    password_salt = column()
    lastest_login = column(datetime.datetime)
    login_fail_count = column(int,is_require=True)








