from typing import Generic, TypeVar, List
from uuid import UUID

from .golden_flag import IsGoldenFlag
from basic_types import NanoType, NanoID

T = TypeVar('T')


class NodeLabel(NanoType[str]):
    pass


class GraphNodeIdentifier(NanoID):
    def __init__(self, label: NodeLabel, _id: UUID):
        super().__init__(_id)
        self.labels = ['NODE', label]

    @property
    def label_string(self) -> str:
        return ':'.join(str(l) for l in self.labels)

T_gni = TypeVar('T_gni',  bound=GraphNodeIdentifier, covariant=True)


class GraphNode(Generic[T_gni]):
    def __init__(self, _id: T_gni, is_golden: IsGoldenFlag):
        self._id: T_gni = _id
        self.is_golden = is_golden

    @property
    def id(self) -> T_gni:
        return self._id

    @property
    def labels(self) -> List[NodeLabel]:
        return self._id.labels

    @property
    def label_string(self) -> str:
        return self.id.label_string