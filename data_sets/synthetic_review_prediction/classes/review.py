from uuid import UUID
from .golden_flag import IsGoldenFlag
from .graph_node import GraphNode, GraphNodeIdentifier, NodeLabel
from .person import PersonID
from .product import ProductID
from basic_types import NanoType


class ReviewID(GraphNodeIdentifier):
    LABEL = NodeLabel('REVIEW')

    def __init__(self, _id: UUID):
        super(ReviewID, self).__init__(self.LABEL, _id)


class ReviewScore(NanoType[float]):
    pass


class Review(GraphNode[ReviewID]):
    def __init__(self,
                 review_id: ReviewID,
                 is_golden: IsGoldenFlag,
                 score: ReviewScore,
                 by_person: PersonID,
                 of_product: ProductID
                 ):
        super(Review, self).__init__(review_id, is_golden)
        self.by_person = by_person
        self.of_product = of_product
        self.score = score


