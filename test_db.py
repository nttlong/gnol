import xsqlalchemy
from xsqlalchemy import qr
import dev_stack
import foxbs
from models import hr
from models import systems
from datetime import datetime
xsqlalchemy.config.set_connection_string(foxbs.settings.CONNECTION_STRING)
xsqlalchemy.create_all()
# try:
qr_dep = qr(hr.Departments)
# ret, error = qr_dep.insert(
#     hr.Departments.name << "TCT",
#     hr.Departments.created_on << datetime.utcnow(),
#     hr.Departments.level << 1,
#     hr.Departments.code << "001"
# )
# qr_dep.where(hr.Departments.code =="001").update(hr.Departments.level_code << "."+ret.id.__str__()+".")

qr_dep.sort(hr.Departments.id.desc)
df = (qr_dep.to_list())
x=df
# print(ret)

# df = qr(Users).where(
#     Users.username == "xxx"
# ).select(
#     Users.username,
#     Users.hash_password
# ).limit(100).where(
#     (Users.id >300) &(Users.id<500)
# ).to_pandas_data_frame()
# x=df
# for i in range(0,100000):
#     qr(Users).insert(dict(
#         email="xxx",
#         username ="dsadas dasdsa",
#         login_fail_count= 0,
#         created_on = datetime.utcnow(),
#         xxx=2
#     ))
#     print(i)
# except Exception as ex:
#     raise ex
# c=1