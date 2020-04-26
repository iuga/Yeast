import pytest
import pandas as pd

from yeast.steps.drop_columns_step import DropColumnsStep
from yeast.errors import YeastValidationError
from yeast.selectors import AllNumeric, AllMatching

from data_samples import startrek_data as data


def test_drop_column_step_must_subset_columns(data):
    """
    Step must subset the correct columns from the df
    """
    step = DropColumnsStep(columns=['year', 'seasons'])
    baked_df = step.prepare(data).bake(data)

    assert len(baked_df.columns) == 4
    assert 'year' not in baked_df.columns
    assert 'seasons' not in baked_df.columns


def test_drop_columns_step_must_fail_if_column_doesnot_exist_on_df(data):
    """
    Raise an exception if any column does not exist
    """
    with pytest.raises(YeastValidationError):
        step = DropColumnsStep(columns=['seasons', 'not_found'])
        step.prepare(data).bake(data)


def test_numerical_selectors_to_drop_columns(data):
    """
    Drop AllNumeric
    """
    step = DropColumnsStep(columns=AllNumeric())
    baked_df = step.prepare(data).bake(data)

    assert len(baked_df.columns) == 4
    assert 'year' not in baked_df.columns
    assert 'rating' not in baked_df.columns


def test_regex_selectors_on_columns(data):
    """
    Test all_numeric
    """
    step = DropColumnsStep(columns=AllMatching('^sea'))
    baked_df = step.prepare(data).bake(data)

    assert len(baked_df.columns) == 5
    assert 'seasons' not in baked_df.columns
