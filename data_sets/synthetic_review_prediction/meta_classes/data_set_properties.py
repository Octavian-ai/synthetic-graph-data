import math
from typing import List, Callable
from ..utils import WeightedOption, choose_weighted_option, get_average_value, Distribution
from ..classes import *
from graph_io.classes.dataset_name import DatasetName


class PersonStyleWeight(WeightedOption[PersonStylePreferenceEnum]):
    pass


class ProductStyleWeight(WeightedOption[ProductStyleEnum]):
    pass


class PersonStyleWeightDistribution(Distribution[PersonStyleWeight, PersonStylePreferenceEnum]):
    pass


class ProductStyleWeightDistribution(Distribution[ProductStyleWeight, ProductStyleEnum]):
    pass


class DataSetProperties(object):
    def __init__(self,
                 dataset_name: DatasetName,
                 n_reviews: int,
                 n_companies: int,
                 reviews_per_product: float,
                 reviews_per_person_distribution: List[WeightedOption[int]],
                 person_styles_distribution: PersonStyleWeightDistribution,
                 product_styles_distribution: ProductStyleWeightDistribution,
                 person_company_number_of_relationships_distribution: [Distribution[WeightedOption[int], int], None],
                 opinion_function: Callable[[Person, Product], ReviewScore],
                 person_style_function: Callable[[PersonStyleWeightDistribution], PersonStylePreferenceVector],
                 product_style_function: Callable[[ProductStyleWeightDistribution], ProductStyleVector]
                 ):
        self.product_style_function = product_style_function
        self.person_style_function = person_style_function
        self.opinion_function = opinion_function
        self.dataset_name = dataset_name
        self.n_companies = n_companies
        self.person_company_number_of_relationships_distribution = person_company_number_of_relationships_distribution
        self.product_styles_distribution = product_styles_distribution
        self.person_styles_distribution: PersonStyleWeightDistribution = person_styles_distribution
        self.reviews_per_person_distribution = reviews_per_person_distribution
        self.reviews_per_product = reviews_per_product
        self.n_reviews = n_reviews

    @property
    def reviews_per_person(self) -> float:
        return get_average_value(self.reviews_per_person_distribution)

    @property
    def n_people(self) -> int:
        return int(math.ceil(float(self.n_reviews) / self.reviews_per_person))

    @property
    def n_products(self) -> int:
        return int(math.ceil(float(self.n_reviews) / self.reviews_per_product))
