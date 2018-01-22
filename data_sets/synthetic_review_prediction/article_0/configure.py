from ..meta_classes import DataSetProperties
from ..meta_classes.data_set_properties import PersonStyleWeightDistribution, PersonStyleWeight, ProductStyleWeight
from ..utils import WeightedOption, Distribution
from ..classes import PersonStylePreferenceEnum, ProductStyleEnum, Style
from ..experiment_1.opinion_function import opinion_function
from ..experiment_1.style_functions import person_style_function, product_style_function
from graph_io.classes.dataset_name import DatasetName

DATASET_NAME = DatasetName('article_0')


def create_data_set_properties() -> DataSetProperties:
    N_STYLES = 2
    styles = [Style(str(i)) for i in range(N_STYLES)]

    for style in styles:
        ProductStyleEnum.register('LIKES_STYLE_'+style.value, style)
        PersonStylePreferenceEnum.register('HAS_STYLE_'+style.value, style)

    data_set_properties = DataSetProperties(
        dataset_name=DATASET_NAME,
        n_reviews=20000,
        reviews_per_product=10,
        reviews_per_person_distribution=[
            WeightedOption[int](1, 0.25),
            WeightedOption[int](2, 0.25),
            WeightedOption[int](3, 0.25),
            WeightedOption[int](4, 0.25)
        ],
        person_styles_distribution=PersonStyleWeightDistribution([
            PersonStyleWeight(x, 1) for x in PersonStylePreferenceEnum.iterate()
        ]),
        product_styles_distribution=Distribution[ProductStyleWeight, ProductStyleEnum]([
            ProductStyleWeight(x, 1) for x in ProductStyleEnum.iterate()
        ]),
        opinion_function=opinion_function,
        person_style_function=person_style_function,
        product_style_function=product_style_function,
        n_companies=0,
        person_company_number_of_relationships_distribution=[]
    )

    return data_set_properties
