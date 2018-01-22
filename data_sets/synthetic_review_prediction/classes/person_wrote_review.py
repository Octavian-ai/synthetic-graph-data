from .graph_edge import GraphEdge, RelationshipName
from .review import ReviewID
from .person import PersonID
from .product import ProductID
from .golden_flag import IsGoldenFlag


class PersonWroteReview(GraphEdge[PersonID, ReviewID]):
    RELATIONSHIP = RelationshipName("WROTE")

    def __init__(self, person_id: PersonID, review_id: ReviewID, is_golden: IsGoldenFlag):
        super(PersonWroteReview, self).__init__(self.RELATIONSHIP, person_id, review_id, is_golden)


class ReviewOfProduct(GraphEdge[ReviewID, ProductID]):
    RELATIONSHIP = RelationshipName("OF")

    def __init__(self, review_id: ReviewID, product_id: ProductID, is_golden: IsGoldenFlag):
        super(ReviewOfProduct, self).__init__(self.RELATIONSHIP, review_id, product_id, is_golden)