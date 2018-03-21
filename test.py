# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            print('before new')
            print(cls)
            cls.__instance = object.__new__(cls, *args, **kwargs)
            print('after new')
            cls.__instance.__Singleton_Init__(*args, **kwargs)
        return cls.__instance

    def __init__(self):
        print("__init__")

    def __Singleton_Init__(self):
        print("__Singleton_Init__")


class BB(Singleton):
    pass


class CC(Singleton):
    pass


c = CC()
c1 = CC()
b = BB()
b.a = 2
c.a = 3
print(id(c), id(c1))
print(b.a, c.a)