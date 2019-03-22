def model(*args,**kwargs):
    def wrapper(*args,**kwargs):
        from .filter import Fields
        return Fields()
    return wrapper