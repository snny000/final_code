import sys


class Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __init__(self):
        pass

    def __setattr__(self, name, value):
            # if name in self.__dict__:
            #     raise self.ConstError, "Can't change config value!"
            if not name.isupper():
                raise self.ConstCaseError, 'config "%s" is not that all letters are capitalized' % name
            self.__dict__[name] = value

sys.modules[__name__] = Const()
