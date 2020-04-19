import pytest
import pandas as pd

from yeast import Recipe
from yeast.steps.group_by_step import GroupByStep
from yeast.steps.summarize_step import SummarizeStep
from yeast.aggregations import AggMean, AggMax, AggMedian, AggSum,
from yeast.aggregations import AggCountDistinct, AggMin, AggCount
from yeast.errors import YeastValidationError
from yeast.selectors import AllNumeric, AllMatching

from data_samples import startrek_data as data


def test_group_by_and_summarize_should_return_a_ready_to_use_dataframe(data):
    """
    Let's group by `seasons` and calculate some aggregations
    """
    recipe = Recipe([
        GroupByStep(['seasons']),
        SummarizeStep({
            'rating_mean': AggMean('rating'),
            'rating_median': AggMedian('rating'),
            'year_max': AggMax('year'),
            'year_min': AggMin('year'),
            'watched_count': AggSum('watched'),
            'years_count': AggCount('year'),
            'years_unique_count': AggCountDistinct('year')
        })
    ])
    baked_df = recipe.prepare(data).bake(data)

    assert 'seasons' in baked_df.columns
    assert 'rating_mean' in baked_df.columns
    assert 'rating_median' in baked_df.columns
    assert 'year_max' in baked_df.columns
    assert 'year_min' in baked_df.columns
    assert 'watched_count' in baked_df.columns
    assert 'years_count' in baked_df.columns
    assert 'years_unique_count' in baked_df.columns
