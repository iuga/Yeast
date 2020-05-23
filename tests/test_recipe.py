import pytest
import pandas as pd

from yeast import Recipe, steps, errors


@pytest.fixture
def raw_data():
    return pd.DataFrame({
        'series_Name': ['Picard', 'TNG', 'Voyager', 'Enterprise', 'Deep Space Nine', 'Discovery'],
        'CreationYear': [2020, 1987, 1995, 2001, 1993, 2017],
        'Total Seasons': [1, 7, 7, 4, 7, 2]
    })


def test_recipe_workflow(raw_data):
    """
    Secuential execution of the recipe
    """
    recipe = Recipe([
        steps.CleanColumnNamesStep('snake'),
        steps.SelectColumnsStep(['creation_year', 'total_seasons'])
    ])
    baked_data = recipe.prepare(raw_data).bake(raw_data)
    assert 'creation_year' in baked_data.columns
    assert 'total_seasons' in baked_data.columns
    assert 'series_name' not in baked_data.columns
    assert 'series_Name' not in baked_data.columns
    assert 'CreationYear' not in baked_data.columns
    assert 'Total Seasons' not in baked_data.columns


def test_recipe_workflow_validations_should_be_on_the_last_transformed_data(raw_data):
    """
    Title exist on the original data but not after the first step.
    Validation on the second step must fail.
    """
    recipe = Recipe([
        steps.SelectColumnsStep(['year', 'seasons']),
        steps.SelectColumnsStep(['title']),
    ])
    with pytest.raises(errors.YeastValidationError):
        recipe.prepare(raw_data).bake(raw_data)


def test_recipe_workflow_only_accepts_yeast_steps(raw_data):
    """
    Currently, we are only going to support Steps objects on the Recipe
    """
    with pytest.raises(errors.YeastRecipeError):
        Recipe([
            steps.SelectColumnsStep(['year', 'seasons']),
            {},
        ])


def test_skip_on_other_set_workflow(raw_data):
    """
    Secuential execution of the recipe but one step (FilterStep) must be skipped on new data
    """
    recipe = Recipe([
        steps.CleanColumnNamesStep('snake'),
        steps.SelectColumnsStep(['creation_year', 'total_seasons']),
        steps.FilterStep('creation_year in [2017, 2020]', role='train')
    ])
    recipe = recipe.prepare(raw_data)

    train = recipe.bake(raw_data)
    assert train.shape == (2, 2)  # Filter Step was applied

    test = recipe.bake(raw_data, role='test')
    assert test.shape == (6, 2)  # Filter Step was applied


def test_custom_roles_workflow(raw_data):
    """
    Different steps with different roles should be executed differently
    """
    recipe = Recipe([
        steps.CleanColumnNamesStep('snake'),
        steps.SelectColumnsStep(['creation_year', 'total_seasons']),
        steps.FilterStep('creation_year == 2020', role='train'),
        steps.SelectColumnsStep(['creation_year'], role='train'),
        steps.SelectColumnsStep(['total_seasons'], role='test'),
    ])
    recipe = recipe.prepare(raw_data)

    train = recipe.bake(raw_data, role='train')
    assert train.shape == (1, 1)  # Filter Step was applied
    assert 'creation_year' in train.columns  # Only creation_year in train role

    test = recipe.bake(raw_data, role='test')
    assert test.shape == (6, 1)  # Filter Step was applied
    assert 'total_seasons' in test.columns  # Only total_seasons in test role
