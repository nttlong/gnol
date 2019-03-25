import xsqlalchemy
from xsqlalchemy import qr
from xsqlalchemy.query2 import select, union, union_all, command

import dev_stack
import foxbs
from models import hr
from models import systems
from datetime import datetime
xsqlalchemy.config.set_connection_string(foxbs.settings.CONNECTION_STRING)
xsqlalchemy.create_all()
# try:
# qr_dep = qr(hr.Departments)
# # ret, error = qr_dep.insert(
# #     hr.Departments.name << "TCT",
# #     hr.Departments.created_on << datetime.utcnow(),
# #     hr.Departments.level << 1,
# #     hr.Departments.code << "001"
# # )
# # qr_dep.where(hr.Departments.code =="001").update(hr.Departments.level_code << "."+ret.id.__str__()+".")
#
# qr_dep.sort(hr.Departments.id.desc).outer_join(
#     hr.Employees, hr.Departments.id == hr.Employees.department_id
# ).outer_join(
#     hr.Employees, (hr.Employees.id==hr.Departments.id) & (hr.Employees.code==hr.Departments.code)
# ).select(
#     hr.Departments.id >> hr.Departments.xxx,
#     hr.Departments.id+2 >> "newid",
#     hr.Departments.name >> "fullname",
#     hr.Employees.code
# )
x= select(systems.Users.email,systems.Users.username)


cmd= command(x)
f= cmd.to_frame()
print f
# x2= select(
#         hr.Employees.id,
#         hr.Departments.id>>"XXX",
#         hr.Employees.code
#     ).outer_join(
#     (hr.Departments.id == hr.Employees.id) & (hr.Employees.id == hr.Departments.code)
# ).where(hr.Employees.code=="XXX")
#
# y= union_all(x,x2,x,x2)
# v=y.group_by(hr.Departments.code)
print (x)
v = command(x).all
print(x)

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
#     ret,error = qr(systems.Users).insert(dict(
#         email="xxx",
#         username ="dsadas dasdsa",
#         login_fail_count= 0,
#         created_on = datetime.utcnow(),
#         xxx=2
#     ))
#     print (error)
#     print(i)
# except Exception as ex:
#     raise ex
# c=1