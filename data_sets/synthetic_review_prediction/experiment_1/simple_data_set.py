from ..meta_classes import DataSetProperties
from ..classes import *
from ..utils import choose_weighted_option
from typing import Set, List, Callable
import random


class SimpleDataSet(object):
    def __init__(self,
                 properties: DataSetProperties
                 ):
        self.product_style_function = properties.product_style_function
        self.person_style_function = properties.person_style_function
        self.opinion_function = properties.opinion_function
        self.properties: DataSetProperties = properties

        self._public_products: List[Product] = list()
        self._public_people_ids: Set[PersonID] = set()
        self._public_review_ids: Set[ReviewID] = set()
        self._public_company_ids: Set[CompanyID] = set()

    def generate_public_companies(self):
        for i in range(self.properties.n_companies):
            company = Company(CompanyID.new_random(), IsGoldenFlag(False))
            self._public_company_ids.add(company.id)
            yield company

    def generate_public_products(self):
        for i in range(self.properties.n_products):
            product_style = ProductStyle(self.product_style_function(self.properties.product_styles_distribution))
            product = Product(ProductID.new_random(), IsGoldenFlag(False), product_style)
            self._public_products.append(product)
            yield product

    def generate_public_people(self):
        properties: DataSetProperties = self.properties
        for i in range(self.properties.n_people):
            number_of_reviews = choose_weighted_option(self.properties.reviews_per_person_distribution)
            number_of_company_opinions = choose_weighted_option(self.properties.person_company_number_of_relationships_distribution)
            meta = PersonMetaProperties(number_of_reviews=number_of_reviews, number_of_company_opinions=number_of_company_opinions)
            style_preference = PersonStylePreference(self.person_style_function(properties.person_styles_distribution))
            person = Person(PersonID.new_random(), IsGoldenFlag(False), style_preference, meta_properties=meta)
            self._public_people_ids.add(person.id)
            yield person

    def generate_reviews(self, person: Person):
        for i in range(person.meta_properties.number_of_reviews):
            product = self.pick_public_product()
            score = self.opinion_function(person, product)
            review = Review(ReviewID.new_random(), IsGoldenFlag(False), score, person.id, product.id)
            self._public_review_ids.add(review.id)
            yield review

    def generate_persons_opinions_of_companies(self, person: Person):
        for i in range(person.meta_properties.number_of_company_opinions):
            company_id = self.pick_public_company()
            if random.choice([True, False]):
                yield PersonLikesCompany(person.id, company_id, is_golden=IsGoldenFlag(False))
            else:
                yield PersonHatesCompany(person.id, company_id, is_golden=IsGoldenFlag(False))

    def pick_public_product(self) -> Product:
        return random.choice(self._public_products)

    def pick_public_person(self) -> PersonID:
        return random.choice(self._public_people_ids)

    def pick_public_company(self) -> CompanyID:
        return random.choice(self._public_company_ids)