from ..utils import choose_weighted_option
from ..classes import *
from ..meta_classes import DataSetProperties, PersonStyleWeightDistribution, ProductStyleWeightDistribution


def product_style_function(product_styles_distribution: ProductStyleWeightDistribution) -> ProductStyleVector:
    return choose_weighted_option(product_styles_distribution).as_vec()


def person_style_function(person_styles_distribution: PersonStyleWeightDistribution) -> PersonStylePreferenceVector:
    return choose_weighted_option(person_styles_distribution).as_vec()

