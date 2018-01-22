from typing import Generic, TypeVar, Iterable, Dict, GenericMeta, List
from numpy import array, int32, ndarray, float32
import abc
T = TypeVar("T")

class DynamicEnumMeta(GenericMeta):
    def __new__(cls, name, bases, namespace, **kwargs):
        return super().__new__(DynamicEnumMeta, name, bases, namespace, **kwargs)

    def __setattr__(self, key, value):
        if key[0] == '_':
            super().__setattr__(key, value)
        else:
            self._register(key, value)
            super().__setattr__(key, value)

class DynamicEnum(Generic[T], metaclass=DynamicEnumMeta):
    _LOCKED = False

    def __hash__(self):
        return self.name.__hash__()

    def __init__(self, defn: T):
        self.defn = defn

    def __neo__(self):
        return self._as_one_hot_list()

    def __eq__(self, other):
        return self.defn == other.defn

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.defn)

    @classmethod
    def parse(cls, name: str):
        candidate = getattr(cls, name.upper())
        assert isinstance(candidate, cls)
        return candidate

    @classmethod
    def register(cls, name: str, value: T):
        setattr(cls, name, cls(value))

    @classmethod
    def _register(cls, name: str, val):
        assert isinstance(val, cls)
        if cls._LOCKED:
            raise Exception('cannot add to locked enum')
        if hasattr(cls, name.upper()):
            raise Exception(f'This enum already has an entry called: {name}')
        val.name = name.upper()

    @classmethod
    def iterate(cls) -> Iterable[T]:
        cls._LOCKED = True
        for k, v in sorted(vars(cls).items()):
            if isinstance(v, cls):
                yield v

    def as_one_hot(self):
        return array(self._as_one_hot_list(), dtype=int32)

    # TODO: memoize this
    def _as_one_hot_list(self):
        cls = self.__class__

        idx = None
        count = 0
        for i, v in enumerate(cls.iterate()):
            if v == self:
                if idx is not None:
                    raise Exception('Same value defined multiple times in enum')
                idx = i
            count = i + 1

        assert count > 0

        out = [1 if i == idx else 0 for i in range(count)]
        assert sum(out) == 1
        return out

    # TODO: memoize this
    def as_vec(self):
        cls = self.__class__

        d = {v: float(1) for v in cls.iterate() if v == self}

        return DynamicEnumVector[cls](d)


T_DynamicEnum = TypeVar("T", bound=DynamicEnum, covariant=True)


class DynamicEnumVector(Generic[T_DynamicEnum]):
    def __init__(self, defn: Dict[T_DynamicEnum, float]):
        self._dict = defn

    def __neo__(self):
        return self.as_list()

    #TODO: cache these
    def as_list(self) -> List[float]:
        my_type = self.__orig_bases__[0]._subs_tree()[1] if not hasattr(self, '__orig_class__') else self.__orig_class__._subs_tree()[1]
        return [self._dict.get(key, 0) for key in my_type.iterate()]

    def as_np_array(self) -> ndarray:
        return array(self.as_list(), dtype=float32)
