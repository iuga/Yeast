import pytest
import pandas as pd

from yeast import Recipe, steps, errors


@pytest.fixture
def raw_data():
    return pd.DataFrame({
        'title': ['Picard', 'TNG', 'Voyager', 'Enterprise', 'Deep Space Nine', 'Discovery'],
        'year': [2020, 1987, 1995, 2001, 1993, 2017],
        'seasons': [1, 7, 7, 4, 7, 2]
    })


def test_recipe_workflow(raw_data):
    """
    Secuential execution of the recipe
    """
    recipe = Recipe([
        steps.SelectColumnStep(['year', 'seasons'])
    ])
    baked_data = recipe.prepare(raw_data).bake(raw_data)
    assert 'year' in baked_data.columns
    assert 'seasons' in baked_data.columns
    assert 'title' not in baked_data.columns


def test_recipe_workflow_validations_should_be_on_the_last_transformed_data(raw_data):
    """
    Title exist on the original data but not after the first step.
    Validation on the second step must fail.
    """
    recipe = Recipe([
        steps.SelectColumnStep(['year', 'seasons']),
        steps.SelectColumnStep(['title']),
    ])
    with pytest.raises(errors.YeastValidationError):
        recipe.prepare(raw_data).bake(raw_data)


def test_recipe_workflow_only_accepts_yeast_steps(raw_data):
    """
    Currently, we are only going to support Steps objects on the Recipe
    """
    with pytest.raises(errors.YeastRecipeError):
        Recipe([
            steps.SelectColumnStep(['year', 'seasons']),
            {},
        ])
