class Session(object):

    cache = {}

    def save_to_cache(self, cache_id, _obj):
        self.cache.update({cache_id: Session.Cell(cache_id, _obj)})

    class Cell(object):

        cache_id = None
        value = None

        def __init__(self, cache_id, _obj):
            self.cache_id = cache_id
            self.value = _obj
