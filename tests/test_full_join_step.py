import pytest
import pandas as pd
from pandas.testing import assert_series_equal

from yeast import Recipe
from yeast.steps import FullJoinStep, SortStep, RenameColumnsStep
from yeast.errors import YeastValidationError

from tests.data_samples import startrek_starships
from tests.data_samples import startrek_starships_specs


def test_full_join_step(startrek_starships, startrek_starships_specs):
    """
    Full Outer Join with NA mismmatches
    """
    recipe = Recipe([
        FullJoinStep(startrek_starships_specs, by="uid"),
        SortStep('uid')
    ])
    baked_data = recipe.prepare(startrek_starships).bake(startrek_starships)

    assert baked_data.shape == (5, 3)
    row = pd.Series({'uid': 'NCC-1031', 'name': 'USS Discovery', 'warp': 9.9}, name=0)
    assert_series_equal(baked_data.loc[0], row)
    row = pd.Series({'uid': 'NX-01', 'name': 'Enterprise', 'warp': None}, name=4)
    assert_series_equal(baked_data.loc[4], row)


def test_full_join_with_using_a_recipe(startrek_starships, startrek_starships_specs):
    """
    Full Outer Join with another Recipe
    """
    right_recipe = Recipe([
        SortStep('uid')
    ])

    left_recipe = Recipe([
        FullJoinStep(right_recipe, by='uid', df=startrek_starships_specs),
        SortStep('uid')
    ])
    baked_df = left_recipe.prepare(startrek_starships).bake(startrek_starships)

    assert baked_df.shape == (5, 3)
    row = pd.Series({'uid': 'NCC-1031', 'name': 'USS Discovery', 'warp': 9.9}, name=0)
    assert_series_equal(baked_df.loc[0], row)
