from uuid import UUID, uuid4
from .graph_node import NodeLabel, GraphNodeIdentifier, GraphNode, IsGoldenFlag
from basic_types import NanoType, NanoID
from .style import Style
from .dynamic_enum import DynamicEnum


class CompanyID(GraphNodeIdentifier):
    LABEL = NodeLabel('Company')

    def __init__(self, _id: UUID):
        super().__init__(self.LABEL, _id)


class Company(GraphNode[CompanyID]):
    pass

