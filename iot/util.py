class ExtensibleEnumMeta(type):
    def __init__(self, name, bases, dict):
        self._value2member_map_ = {}
        for k, v in dict.items():
            if k.startswith('_'):
                continue
            if callable(v):
                continue
            if isinstance(v, property):
                continue
            instance = self(v)
            instance.name = k
            setattr(self, k, instance)
        type.__init__(self, name, bases, dict)

    def __call__(self, value):
        if isinstance(value, self):
            return value
        if value not in self._value2member_map_:
            self._value2member_map_[value] = super(ExtensibleEnumMeta, self).__call__(value)
        return self._value2member_map_[value]

class ExtensibleIntEnum(int, metaclass=ExtensibleEnumMeta):
    """Similar to Python3.4's enum.IntEnum, this type can be used for named
    numbers which are not comprehensively known, like CoAP option numbers."""

    def __add__(self, delta):
        return type(self)(int(self) + delta)

    def __repr__(self):
        return '<%s %d>'%(type(self).__name__, self)