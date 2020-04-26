import pytest
import pandas as pd
from pandas.testing import assert_series_equal

from yeast import Recipe
from yeast.steps import LeftJoinStep, SortStep, RenameColumnsStep
from yeast.errors import YeastValidationError

from tests.data_samples import startrek_starships
from tests.data_samples import startrek_starships_specs


def test_left_join_step(startrek_starships, startrek_starships_specs):
    """
    Left Join with NA mismmatches
    """
    recipe = Recipe([
        LeftJoinStep(startrek_starships_specs, by="uid"),
        SortStep('uid')
    ])
    baked_data = recipe.prepare(startrek_starships).bake(startrek_starships)

    row = pd.Series({'uid': 'NCC-1031', 'name': 'USS Discovery', 'warp': 9.9}, name=0)
    assert_series_equal(baked_data.loc[0], row)
    row = pd.Series({'uid': 'NX-01', 'name': 'Enterprise', 'warp': None}, name=4)
    assert_series_equal(baked_data.loc[4], row)


def test_left_join_with_using_a_recipe(startrek_starships, startrek_starships_specs):
    """
    Left Join with another Recipe
    """
    right_recipe = Recipe([
        SortStep('uid')
    ])

    left_recipe = Recipe([
        LeftJoinStep(right_recipe, by='uid', df=startrek_starships_specs),
        SortStep('uid')
    ])
    baked_df = left_recipe.prepare(startrek_starships).bake(startrek_starships)

    row = pd.Series({'uid': 'NCC-1031', 'name': 'USS Discovery', 'warp': 9.9}, name=0)
    assert_series_equal(baked_df.loc[0], row)


def test_left_join_without_by_workflow(startrek_starships, startrek_starships_specs):
    """
    Left Join without pass the column names
    """
    recipe = Recipe([
        LeftJoinStep(startrek_starships_specs),
        SortStep('uid')
    ])
    baked_data = recipe.prepare(startrek_starships).bake(startrek_starships)

    row = pd.Series({'uid': 'NCC-1031', 'name': 'USS Discovery', 'warp': 9.9}, name=0)
    assert_series_equal(baked_data.loc[0], row)


def test_left_join_column_not_found_left_thus_fail(startrek_starships, startrek_starships_specs):
    """
    Left Join but the column uid does not exist on left
    """
    recipe = Recipe([
        RenameColumnsStep({'uid': 'not_found'}),
        LeftJoinStep(startrek_starships_specs, by='uid')
    ])

    with pytest.raises(YeastValidationError):
        recipe.prepare(startrek_starships).bake(startrek_starships)


def test_left_join_column_not_found_right_thus_fail(startrek_starships, startrek_starships_specs):
    """
    Left Join but the column uid does not exist on right
    """
    right_recipe = Recipe([
        RenameColumnsStep({'uid': 'not_found'})
    ])
    baked_specs = right_recipe.prepare(startrek_starships_specs).bake(startrek_starships_specs)

    recipe = Recipe([
        LeftJoinStep(baked_specs, by='uid')
    ])

    with pytest.raises(YeastValidationError):
        recipe.prepare(startrek_starships).bake(startrek_starships)


def test_left_join_using_df_but_not_a_recipe(startrek_starships, startrek_starships_specs):
    """
    df is only used if right is a Recipe
    """
    recipe = Recipe([
        LeftJoinStep(startrek_starships_specs, by="uid", df=startrek_starships)
    ])

    with pytest.raises(YeastValidationError) as ex:
        recipe.prepare(startrek_starships).bake(startrek_starships)
