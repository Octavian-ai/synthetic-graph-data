class CypherQuery(object):
    def __init__(self, value: str):
        self.value = value.replace('\t', ' ')