from xsqlalchemy import column,table


@table("sys_language_resources")
class SysLanguageResource(object):
    id = column(data_type=int, is_primary= True)
    language_code = column(data_type=str,data_len=2, is_require= True)
    app_name = column(data_len=100, is_require=True)
    view_path = column(data_len=300, is_require=True)
    key = column(data_len=300, is_require= True)
    value = column(data_len= 4000, is_require=True)


