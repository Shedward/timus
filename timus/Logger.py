class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class Log(object, metaclass=Singleton):
    """Simple logger"""

    ''' Show only error messages '''
    Err = 0
    ''' Show also basic messages '''
    Msg = 1
    ''' Show all '''
    Vrb = 2

    def __init__(self, lvl=Err):
        super(Log, self).__init__()
        self.lvl = lvl

    def __call__(self, lvl=1, *args):
        if lvl <= self.lvl:
            print(*args)
