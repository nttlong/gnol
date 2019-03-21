class Column(object):

    def __init__(self,field,caption = None, dropdown = None, format = None ,is_lock = None):
        self.field = field
        if not caption:
            caption = field
        self.caption = caption
        self.dropdown = dropdown
        self.format = format
        self.is_lock = is_lock

