from xsqlalchemy import table, column, create_index
import datetime
from . base import BaseTable


@table("sys_users")
class Users(BaseTable):
    username = column(data_len=60, is_require=True, is_unique=True)
    email = column(is_unique=True)
    hash_password = column(data_len=3200)
    password_salt = column(data_len=100)

    lastest_login = column(datetime.datetime)
    login_fail_count = column(int, is_require=True)


create_index(Users,True,Users.username)
create_index(Users,True,Users.email)






