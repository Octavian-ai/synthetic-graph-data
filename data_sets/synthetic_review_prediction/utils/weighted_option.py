from functools import reduce
from random import random
from typing import List, Generic, TypeVar, Dict
from math import pow

T__ = TypeVar('T__', contravariant=True)


class WeightedOption(Generic[T__]):
    def __init__(self, option: T__, weight: float=1.0):
        self.weight = weight
        self.option = option


T_w = TypeVar('T_w', bound=WeightedOption[T__])


class Distribution(Generic[T_w, T__]):
    def __init__(self, entries: List[T_w]):
        self.list = list(entries)

    def __getitem__(self, index):
        result = self.list[index]
        return result


T_ = TypeVar('T_')

T_L = TypeVar('T_L', bound=List[WeightedOption[T_]], covariant=True)


def choose_weighted_option(options: T_L) -> T_:
    total_weights = float(sum(x.weight for x in options))

    def get_decision_boundaries() -> (float, T_):
        current = 0
        for weighted_option in options:
            current += weighted_option.weight / total_weights
            yield current, weighted_option.option

    decision_point = random()

    for boundary, option in get_decision_boundaries():
        if decision_point <= boundary:
            return option


def random_scores_from_distribution(options: T_L) -> Dict[T_, float]:

    def get_normalised_scores() -> (float, T_):
        buffer = [(random() * float(weighted_option.weight), weighted_option.option) for weighted_option in options]

        for score, option in buffer:
            yield score, option #This should return an array of values between 0 and 1

    return {k:v for v,k in get_normalised_scores()}


def get_average_value(options: List[WeightedOption[int]]) -> float:
    total_weights = float(sum(x.weight for x in options))

    return reduce(lambda x,y: x + y.weight * float(y.option), options, 0.0) / total_weights
