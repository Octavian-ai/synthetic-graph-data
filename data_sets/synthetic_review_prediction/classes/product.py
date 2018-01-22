from uuid import UUID, uuid4
from .graph_node import NodeLabel, GraphNodeIdentifier, GraphNode, IsGoldenFlag
from basic_types import NanoType, NanoID
from .style import Style
from .dynamic_enum import DynamicEnum, DynamicEnumVector


class ProductID(GraphNodeIdentifier):
    LABEL = NodeLabel('PRODUCT')

    def __init__(self, _id: UUID):
        super().__init__(self.LABEL, _id)


class ProductStyleEnum(DynamicEnum[Style]):

    @property
    def style(self):
        return self.defn


class ProductStyleVector(DynamicEnumVector[ProductStyleEnum]):
    @property
    def style(self):
        return self.as_np_array()


class ProductStyle(NanoType[ProductStyleEnum]):
    pass


class Product(GraphNode[ProductID]):
    def __init__(self,
                 product_id: ProductID,
                 is_golden: IsGoldenFlag,
                 style: ProductStyle
                 ):
        super(Product, self).__init__(product_id, is_golden)
        self.style = style


