# Minimal stub for the `discord` package used by gepaw channels.

class _Dummy:
    def __init__(self, *a, **kw):
        pass

    def __getattr__(self, name):
        return _Dummy()

    def __call__(self, *a, **kw):
        return _Dummy()


class Intents(_Dummy):
    @classmethod
    def default(cls):
        return cls()


class Client(_Dummy):
    pass


class Thread(_Dummy):
    pass


class File(_Dummy):
    pass
