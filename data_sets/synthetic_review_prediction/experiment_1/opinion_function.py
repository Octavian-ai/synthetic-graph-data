from ..classes import Person, Product, ReviewScore
from numpy import ndarray


def opinion_function(person: Person, product: Product) -> ReviewScore:

    person_style = person.style_preference.value.as_np_array()
    assert isinstance(person_style, ndarray)

    product_style = product.style.value.as_np_array()
    assert isinstance(product_style, ndarray)

    review_score = float(person_style.dot(product_style))/person_style.sum()

    return ReviewScore(review_score)
