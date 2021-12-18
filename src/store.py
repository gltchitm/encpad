class Store:
    def __init__(self):
        self.values = {}
    def __setitem__(self, key, value):
        if key in self.values and key.isupper() and len(key) > 2:
            raise AttributeError(f'cannot modify constant value \'{key}\'')
        self.values[key] = value
    def __getitem__(self, key):
        return self.values.get(key)

store = Store()
