from ..meta_classes import DataSetProperties
from ..meta_classes.data_set_properties import PersonStyleWeightDistribution, PersonStyleWeight, ProductStyleWeight
from ..utils import WeightedOption, Distribution
from ..classes import PersonStylePreferenceEnum, ProductStyleEnum, Style
from graph_io.classes.dataset_name import DatasetName
from ..experiment_1.opinion_function import opinion_function
from ..experiment_1.style_functions import product_style_function, person_style_function

DATASET_NAME = DatasetName('article_1')


def create_data_set_properties() -> DataSetProperties:
    
    n_styles = 6
    n_products = 100
    reviews_per_product = 1000
    reviews_per_person = 40

    styles = [Style(str(i)) for i in range(n_styles)]

    for style in styles:
        ProductStyleEnum.register('LIKES_'+style.value, style)
        PersonStylePreferenceEnum.register('HAS_'+style.value, style)

    data_set_properties = DataSetProperties(
        dataset_name=DATASET_NAME,
        n_reviews=n_products * reviews_per_product,
        n_companies=0,
        reviews_per_product=reviews_per_product,
        reviews_per_person_distribution=[
            WeightedOption[int](reviews_per_person, 1)
        ],
        person_styles_distribution=PersonStyleWeightDistribution([
            PersonStyleWeight(x, 1) for x in PersonStylePreferenceEnum.iterate()
        ]),
        product_styles_distribution=Distribution[ProductStyleWeight, ProductStyleEnum]([
            ProductStyleWeight(x, 1) for x in ProductStyleEnum.iterate()
        ]),
        person_company_number_of_relationships_distribution=[],
        opinion_function=opinion_function,
        person_style_function=person_style_function,
        product_style_function=product_style_function
    )

    return data_set_properties
