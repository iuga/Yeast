import pytest
import numpy as np

from yeast import Recipe
from yeast.steps import ConstantImputeStep, MutateStep
from yeast.errors import YeastValidationError, YeastBakeError, YeastPreparationError
from yeast.transformers import MapValues

from data_samples import startrek_data as data


def test_constant_inputation_on_numerical_column(data):
    """
    Before impute the season, replace some values with NAN to have some missing information
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
        ConstantImputeStep(['seasons', 'rating'], value=0)
    ])
    bdf = recipe.prepare(data).bake(data)

    seasons = bdf['seasons'].round(1).tolist()
    assert seasons[0] == 1.0
    assert seasons[1] == 0.0  # k
    assert seasons[2] == 0.0  # k
    assert seasons[3] == 4.0
    assert seasons[4] == 0.0  # k
    assert seasons[5] == 2.0

    ratings = bdf['rating'].round(1).tolist()
    assert ratings[0] == 0.0  # k
    assert ratings[1] == 0.0  # k
    assert ratings[2] == 7.4
    assert ratings[3] == 6.8
    assert ratings[4] == 8.9
    assert ratings[5] == 0.0  # k


def test_mean_inputation_on_a_categorical_column(data):
    """
    We can not calculate the mean on a non-numerical column.
    """
    recipe = Recipe([
        MutateStep({
            'title': MapValues({
                'Voyager': np.NaN
            })
        }),
        ConstantImputeStep(['title'], value="Other")
    ])
    bdf = recipe.prepare(data).bake(data)

    titles = bdf['title'].tolist()
    assert titles[0] == 'Picard'
    assert titles[1] == 'TNG'
    assert titles[2] == 'Other'
    assert titles[3] == 'Enterprise'
    assert titles[4] == 'Deep Space Nine'
    assert titles[5] == 'Discovery'


def test_if_column_does_not_exist_raises_an_error(data):
    """
    Only use existent columns
    """
    step = ConstantImputeStep(['not_found'], value='does_not_matter')

    with pytest.raises(YeastValidationError):
        step.prepare(data)
