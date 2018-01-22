from typing import Generic, TypeVar
from basic_types import NanoType
from .graph_node import GraphNode, GraphNodeIdentifier
from .golden_flag import IsGoldenFlag

T_from = TypeVar('T_from', GraphNode, GraphNodeIdentifier)
T_to = TypeVar('T_to', GraphNode, GraphNodeIdentifier)


class EdgeType(NanoType[str]):
    pass


class RelationshipName(NanoType[str]):
    pass


class GraphEdge(Generic[T_from, T_to]):
    def __init__(self, relationship: RelationshipName, _from: T_from, to: T_to, is_golden: IsGoldenFlag):
        assert _from is not None
        assert to is not None
        assert relationship is not None

        self.is_golden = is_golden
        self._from = _from
        self._to = to
        self.relationship = relationship
