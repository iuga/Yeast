import pytest
import numpy as np

from yeast import Recipe
from yeast.steps import MedianImputeStep, MutateStep
from yeast.errors import YeastValidationError, YeastBakeError, YeastPreparationError
from yeast.transformers import MapValues

from data_samples import startrek_data as data


def test_median_inputation_on_numerical_column(data):
    """
    Before impute the season, replace 7 with NAN to have some missing values
    """
    recipe = Recipe([
        MutateStep({
            'seasons': MapValues({
                7: np.NaN
            }),
            'rating': MapValues({
                9.3: np.NaN,
                9.9: np.NaN,
                9.0: np.NaN
            })
        }),
        MedianImputeStep(['seasons', 'rating'])
    ])
    bdf = recipe.prepare(data).bake(data)

    # [1.0, 2.0, 2.0, 4.0, 2.0, 2.0]
    seasons = bdf['seasons'].round(1).tolist()
    assert seasons[0] == 1.0
    assert seasons[1] == 2.0  # median
    assert seasons[2] == 2.0  # median
    assert seasons[3] == 4.0
    assert seasons[4] == 2.0  # median
    assert seasons[5] == 2.0

    # [7.4, 7.4, 7.4, 6.8, 8.9, 7.4]
    ratings = bdf['rating'].round(1).tolist()
    assert ratings[0] == 7.4  # median
    assert ratings[1] == 7.4  # median
    assert ratings[2] == 7.4
    assert ratings[3] == 6.8
    assert ratings[4] == 8.9
    assert ratings[5] == 7.4  # median


def test_if_column_does_not_exist_raises_an_error(data):
    """
    Only use existent columns
    """
    step = MedianImputeStep(['not_found'])

    with pytest.raises(YeastValidationError):
        step.prepare(data)


def test_if_bake_and_not_prepare_should_raise_an_error(data):
    """
    If we are baking without preparation we should have an error
    """
    step = MedianImputeStep(['not_found'])

    with pytest.raises(YeastBakeError):
        step.bake(data)


def test_median_inputation_on_a_non_numerical_column_must_fail(data):
    """
    We can not calculate the median on a non-numerical column.
    """
    recipe = Recipe([
        MutateStep({
            'title': MapValues({
                'Voyager': np.NaN
            })
        }),
        MedianImputeStep(['title'])
    ])

    with pytest.raises(YeastPreparationError):
        recipe.prepare(data)
