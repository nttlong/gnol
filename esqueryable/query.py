
__models__ = None

class qr():
    def __init__(self,cnn):
        from elasticsearch import Elasticsearch
        self.es = Elasticsearch(cnn)

    def create_index(self,name):
        if self.es.indices.exists(name):
            return qr_index(self,name)
        else:
            self.es.indices.create(name)
            return qr_index(self,name)

    def get_all_indexes(self):
        from . dynamic_object import dynamic_object
        obj = self.es.indices.get_alias("*")
        ret = []
        for k,v in obj.items():
            ret.append(
                dynamic_object(dict(
                    name=k,
                    value = v
                ))
            )
        return ret


class qr_index():
    def __init__(self,_qr,name):
        self.qr =_qr
        self.name = name

    def get_mapping(self):
        from elasticsearch import Elasticsearch
        if isinstance(self.qr.es, Elasticsearch):
            return self.qr.es.indices.get_mapping(self.name)

    def get_mapping_as_object(self):
        from . dynamic_object import dynamic_object
        ret = self.get_mapping()
        if ret[self.name]:
            return dynamic_object(ret[self.name]['mappings'])

    def get_properties(self):
        global __models__
        if not __models__:
            __models__ ={}
        if not __models__.get(self.name, None):
            ret =self.get_mapping()
            __models__.update(
                {
                    self.name: ret[self.name]['mappings']
                }
            )
        return __models__[self.name]

    def get_all_docs(self,page_index = 0, page_size = 1000):
        res = self.qr.es.search(index=self.name, body={
            'size': page_size,
            'query': {
                'match_all': {}
            }
        })
        return res

    def search(self,fields=None,doc_type=None,page_size=50, page_index=0):
        from elasticsearch import Elasticsearch

        from .filter import get_elasticsearch_filter

        _from = page_index*page_size
        size = page_size

        """
        "from": 0,
    "size": 1
        """

        _filter = get_elasticsearch_filter(fields)
        if not _filter:
            _filter={
                "from": _from,
                "size": size
            }
        else:
            _filter.update({
                "from": _from,
                "size": size
            })
        # # _filter = where(_filter)
        if isinstance(self.qr.es, Elasticsearch):
            ret = self.qr.es.search(self.name, doc_type=doc_type, body=_filter)
            if ret.get('hits'):
                if ret['hits'].get('hits'):
                    ret_data = dict(
                        items=ret['hits']['hits'],
                        total=ret['hits']['total'],
                        page_size=page_size,
                        page_index=page_index
                    )
                    return ret_data

        return dict(
            items=[],
            total=0,
            page_size=page_size,
            page_index = page_index
        )

    def search_as_objects(self,fields=None,doc_type=None,page_size=50, page_index=0):
        from .dynamic_object import dynamic_object
        return dynamic_object(self.search(fields,doc_type, page_size, page_index))

    def delete(self,id):
        from .filter import Fields
        from elasticsearch import Elasticsearch
        ret = self.search_as_objects(Fields()._id == id)
        if ret.items.__len__() == 0:
            return None,"Item was not found"
        if isinstance(self.qr.es,Elasticsearch):
            bulk_body = [
                '{{"delete": {{"_index": "{}", "_type": "{}", "_id": "{}"}}}}'
                    .format(self.name, ret.items[0]._type, id)]

            ret = self.qr.es.bulk('\n'.join(bulk_body))

            return ret, None

