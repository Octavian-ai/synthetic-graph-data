from typing import Generic, TypeVar
from uuid import uuid4, UUID

T = TypeVar('T')


class NanoType(Generic[T]):
    def __init__(self, value: [T]):
        self._value: T = value

    @property
    def value(self) -> T:
        return self._value

    def __hash__(self):
        return self._value.__hash__()

    def __eq__(self, other):
        if isinstance(other, NanoType):
            return self._value.__eq__(other._value)
        return self._value.__eq__(other)

    def __ne__(self, other):
        return self._value.__ne__(other)

    def __gt__(self, other):
        return self._value.__gt__(other)

    def __lt__(self, other):
        return self._value.__lt__(other)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class NanoID(NanoType[UUID]):

    @property
    def id(self) -> NanoType:
        return self

    @classmethod
    def new_random(cls):
        return cls(uuid4())