class Singleton:
    _instance = None

    def __init__(self, decorated):
        self._decorated = decorated

    def get_instance(self):
        if Singleton._instance is None:
            Singleton._instance = self._decorated()
        return Singleton._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `get_instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)