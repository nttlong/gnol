from .query import qr
from .filter import Fields
from .models import model


@model()
class CourseWare():
    class course_info():
        modes= str
        language =str
        start = str
        number = str
        org = str
        # class content():
        #     short_description = str
        #     overview =str
        #     display_name =str
        #     number =str
        #     course = str
        #     image_url = str
        #     org =str









q = qr(["172.16.7.63:9200"]).create_index("courseware_index")
properties = q.get_properties()
lst = q.search_as_objects(fields=(
     (CourseWare.course_info.org=="LV")
))
ret =q.delete(lst.items[0]._id)
print ret

