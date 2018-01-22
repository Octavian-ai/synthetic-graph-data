from .graph_edge import GraphEdge, RelationshipName
from .person import PersonID
from .company import CompanyID
from .golden_flag import IsGoldenFlag


class PersonLikesCompany(GraphEdge[PersonID, CompanyID]):
    RELATIONSHIP = RelationshipName("LIKES")

    def __init__(self, person_id: PersonID, company_id: CompanyID, is_golden: IsGoldenFlag):
        super(PersonLikesCompany, self).__init__(self.RELATIONSHIP, person_id, company_id, is_golden)


class PersonHatesCompany(GraphEdge[PersonID, CompanyID]):
    RELATIONSHIP = RelationshipName("HATES")

    def __init__(self, person_id: PersonID, company_id: CompanyID, is_golden: IsGoldenFlag):
        super(PersonHatesCompany, self).__init__(self.RELATIONSHIP, person_id, company_id, is_golden)
