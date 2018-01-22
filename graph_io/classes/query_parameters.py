from uuid import UUID


class QueryParams(object):
    def __init__(self, **kwargs):
        self._params = kwargs

    def update(self,other):
        self._params.update(other._params)

    @property
    def query_string(self):
        return "{" + ", ".join(f"{name}: ${name}" for name in self._params) + "}"

    def union(self, other):
        return QueryParams(**self._params, **other._params)

    def __extract_neo_value(self, element):
        assert element is not None

        if hasattr(element, '__neo__'):
            return element.__neo__()
        if hasattr(element, 'value'):
            return self.__extract_neo_value(element.value)
        if isinstance(element, UUID):
            return str(element)
        return element

    @property
    def cypher_query_parameters(self):
        return {n: self.__extract_neo_value(p) for n,p in self._params.items()} if self._params else {}

    # All this wrapping seems boilerplate to David and he dislikes it
    def __getitem__(self, index):
        return self._params[index]

    def __str__(self):
        return str(self._params)

    def __repr__(self):
        return self.__str__()
