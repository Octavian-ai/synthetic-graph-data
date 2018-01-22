from uuid import UUID, uuid4
from .graph_node import GraphNodeIdentifier, GraphNode, NodeLabel, IsGoldenFlag
from basic_types import NanoID, NanoType
from .style import Style
from .dynamic_enum import DynamicEnum, DynamicEnumVector

class PersonID(GraphNodeIdentifier):
    LABEL = NodeLabel('PERSON')

    def __init__(self, _id: UUID):
        super().__init__(self.LABEL, _id)


class PersonStylePreferenceEnum(DynamicEnum[Style]):
    @property
    def style(self):
        return self.defn


class PersonStylePreferenceVector(DynamicEnumVector[PersonStylePreferenceEnum]):
    pass


class PersonStylePreference(NanoType[PersonStylePreferenceVector]):
    pass


class PersonMetaProperties(object):
    def __init__(self, number_of_reviews: int, number_of_company_opinions: int):
        self.number_of_company_opinions = number_of_company_opinions
        self.number_of_reviews = number_of_reviews


class Person(GraphNode[PersonID]):
    def __init__(self,
                 person_id: PersonID,
                 is_golden: IsGoldenFlag,
                 style_preference: PersonStylePreference,
                 meta_properties: PersonMetaProperties=None
                 ):
        super(Person, self).__init__(person_id, is_golden)
        self.style_preference = style_preference
        self.meta_properties = meta_properties
