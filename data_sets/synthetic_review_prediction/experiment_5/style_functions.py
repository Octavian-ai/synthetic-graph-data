from ..utils import random_scores_from_distribution
from ..classes import *
from ..meta_classes import ProductStyleWeightDistribution, PersonStyleWeightDistribution


def person_style_function(properties: PersonStyleWeightDistribution) -> PersonStylePreferenceVector:
    return PersonStylePreferenceVector(random_scores_from_distribution(properties))


def product_style_function(properties: ProductStyleWeightDistribution) -> ProductStyleVector:
    return ProductStyleVector(random_scores_from_distribution(properties))

