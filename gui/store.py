class Store:
    def __init__(self):
        self.values = {}
    def set_value(self, key, value):
        self.values[key] = value
    def get_value(self, key):
        if key in self.values:
            return self.values[key]

store = Store()