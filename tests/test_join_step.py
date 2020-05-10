import pytest
import pandas as pd
from pandas.testing import assert_series_equal

from yeast import Recipe
from yeast.steps import JoinStep, SortStep, RenameColumnsStep
from yeast.errors import YeastValidationError

from tests.data_samples import startrek_starships
from tests.data_samples import startrek_starships_specs


def test_join_on_left_step(startrek_starships, startrek_starships_specs):
    """
    Left Join with NA mismmatches
    """
    recipe = Recipe([
        JoinStep(startrek_starships_specs, by="uid", how="left"),
        SortStep('uid')
    ])
    baked_data = recipe.prepare(startrek_starships).bake(startrek_starships)

    assert baked_data.shape == (5, 3)
    row = pd.Series({'uid': 'NCC-1031', 'name': 'USS Discovery', 'warp': 9.9}, name=0)
    assert_series_equal(baked_data.loc[0], row)
    row = pd.Series({'uid': 'NX-01', 'name': 'Enterprise', 'warp': None}, name=4)
    assert_series_equal(baked_data.loc[4], row)

def test_join_on_inner_step(startrek_starships, startrek_starships_specs):
    """
    Inner Join with NA mismmatches
    """
    recipe = Recipe([
        JoinStep(startrek_starships_specs, by="uid", how="inner"),
        SortStep('uid')
    ])
    baked_data = recipe.prepare(startrek_starships).bake(startrek_starships)

    assert baked_data.shape == (4, 3)
    row = pd.Series({'uid': 'NCC-1031', 'name': 'USS Discovery', 'warp': 9.9}, name=0)
    assert_series_equal(baked_data.loc[0], row)
    row = pd.Series({'uid': 'NCC-74656', 'name': 'USS Voyager', 'warp': 9.975}, name=3)
    assert_series_equal(baked_data.loc[3], row)


def test_join_on_right_step(startrek_starships, startrek_starships_specs):
    """
    Right Join with NA mismmatches
    """
    recipe = Recipe([
        JoinStep(startrek_starships_specs, by="uid", how="right"),
        SortStep('uid')
    ])
    baked_data = recipe.prepare(startrek_starships).bake(startrek_starships)

    assert baked_data.shape == (4, 3)
    row = pd.Series({'uid': 'NCC-1031', 'name': 'USS Discovery', 'warp': 9.9}, name=0)
    assert_series_equal(baked_data.loc[0], row)
    row = pd.Series({'uid': 'NCC-74656', 'name': 'USS Voyager', 'warp': 9.975}, name=3)
    assert_series_equal(baked_data.loc[3], row)


def test_join_on_fullouter_step(startrek_starships, startrek_starships_specs):
    """
    Full outer Join with NA mismmatches
    """
    recipe = Recipe([
        JoinStep(startrek_starships_specs, by="uid", how="full"),
        SortStep('uid')
    ])
    baked_data = recipe.prepare(startrek_starships).bake(startrek_starships)

    assert baked_data.shape == (5, 3)
    row = pd.Series({'uid': 'NCC-1031', 'name': 'USS Discovery', 'warp': 9.9}, name=0)
    assert_series_equal(baked_data.loc[0], row)
    row = pd.Series({'uid': 'NX-01', 'name': 'Enterprise', 'warp': None}, name=4)
    assert_series_equal(baked_data.loc[4], row)


def test_join_on_invalid_how_step(startrek_starships, startrek_starships_specs):
    """
    The how parameter is invalid and the step shoul fail the validation
    """
    recipe = Recipe([
        JoinStep(startrek_starships_specs, by="uid", how="not_exist"),
    ])
    with pytest.raises(YeastValidationError) as ex:
        recipe.prepare(startrek_starships).bake(startrek_starships)


def test_left_join_with_using_a_recipe(startrek_starships, startrek_starships_specs):
    """
    Left Join with another Recipe
    """
    right_recipe = Recipe([
        SortStep('uid')
    ])

    left_recipe = Recipe([
        JoinStep(right_recipe, by='uid', how='left',  df=startrek_starships_specs),
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
        JoinStep(startrek_starships_specs, how="left"),
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
        JoinStep(startrek_starships_specs, by='uid', how="left")
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
        JoinStep(baked_specs, by='uid', how="left")
    ])

    with pytest.raises(YeastValidationError):
        recipe.prepare(startrek_starships).bake(startrek_starships)


def test_left_join_using_df_but_not_a_recipe(startrek_starships, startrek_starships_specs):
    """
    df is only used if right is a Recipe
    """
    recipe = Recipe([
        JoinStep(startrek_starships_specs, by="uid", df=startrek_starships, how="left")
    ])

    with pytest.raises(YeastValidationError) as ex:
        recipe.prepare(startrek_starships).bake(startrek_starships)
