import pytest
import numpy as np

from yeast.steps.cast_columns_step import CastColumnsStep
from yeast.errors import YeastValidationError

from data_samples import startrek_data as data


def test_column_casting(data):
    """
    Test the most basic column casting
    """
    step = CastColumnsStep({
        'title': 'string',
        'year': 'integer',
        'seasons': 'integer',
        'watched': 'boolean',
        'rating': 'float',
        'aired': 'datetime'
    })

    # Remove the dtypes
    data = data.astype({
        'title': 'object',
        'year': 'object',
        'seasons': 'object',
        'watched': 'object',
        'rating': 'object',
        'aired': 'object'
    })

    baked_df = step.prepare(data).bake(data)

    assert baked_df['title'].dtype.kind == 'O'
    assert baked_df['year'].dtype.kind == 'i'
    assert baked_df['seasons'].dtype.kind == 'i'
    assert baked_df['watched'].dtype.kind == 'b'
    assert baked_df['rating'].dtype.kind == 'f'
    assert baked_df['aired'].dtype.kind == 'M'


def test_column_casting_with_unexistent_column(data):
    """
    One of the columns does not exist
    """
    step = CastColumnsStep({
        'title': 'string',
        'not_found': 'integer',
        'watched': 'boolean'
    })
    with pytest.raises(YeastValidationError):
        baked_df = step.prepare(data).bake(data)


def test_column_casting_with_unexistent_dtype(data):
    """
    One of the dtypes does not exist
    """
    step = CastColumnsStep({
        'title': 'string',
        'rating': 'megaplot',
        'watched': 'boolean'
    })
    with pytest.raises(YeastValidationError):
        baked_df = step.prepare(data).bake(data)
