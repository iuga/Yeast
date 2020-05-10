import pytest
import pandas as pd
from pandas.testing import assert_series_equal

from yeast import Recipe
from yeast.steps import RightJoinStep, SortStep, RenameColumnsStep
from yeast.errors import YeastValidationError

from tests.data_samples import startrek_starships
from tests.data_samples import startrek_starships_specs


def test_right_join_step(startrek_starships, startrek_starships_specs):
    """
    Right Join with NA mismmatches
    """
    recipe = Recipe([
        RightJoinStep(startrek_starships_specs, by="uid"),
        SortStep('uid')
    ])
    bdf = recipe.prepare(startrek_starships).bake(startrek_starships)

    assert bdf.shape == (4, 3)
    row = pd.Series({'uid': 'NCC-1031', 'name': 'USS Discovery', 'warp': 9.9}, name=0)
    assert_series_equal(bdf.loc[0], row)
    row = pd.Series({'uid': 'NCC-74656', 'name': 'USS Voyager', 'warp': 9.975}, name=3)
    assert_series_equal(bdf.loc[3], row)


def test_right_join_with_using_a_recipe(startrek_starships, startrek_starships_specs):
    """
    Right Join with another Recipe
    """
    right_recipe = Recipe([
        SortStep('uid')
    ])

    left_recipe = Recipe([
        RightJoinStep(right_recipe, by='uid', df=startrek_starships_specs),
        SortStep('uid')
    ])
    bdf = left_recipe.prepare(startrek_starships).bake(startrek_starships)

    assert bdf.shape == (4, 3)
    row = pd.Series({'uid': 'NCC-1031', 'name': 'USS Discovery', 'warp': 9.9}, name=0)
    assert_series_equal(bdf.loc[0], row)
    row = pd.Series({'uid': 'NCC-74656', 'name': 'USS Voyager', 'warp': 9.975}, name=3)
    assert_series_equal(bdf.loc[3], row)
