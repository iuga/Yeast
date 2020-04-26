import pytest
import pandas as pd

from yeast.steps.select_columns_step import SelectColumnsStep
from yeast.errors import YeastValidationError
from yeast.selectors import AllNumeric, AllMatching

from data_samples import startrek_data as data


def test_select_column_step_must_subset_columns_using_column_names(data):
    """
    Step must subset the correct columns from the df using a list of columns
    """
    step = SelectColumnsStep(columns=['year', 'seasons'])
    baked_df = step.prepare(data).bake(data)

    assert len(baked_df.columns) == 2
    assert 'year' in baked_df.columns
    assert 'seasons' in baked_df.columns


def test_select_column_step_must_allow_selectors_and_column_names(data):
    """
    Step must subset the correct columns using a Selector and Column names
    """
    step = SelectColumnsStep(columns=[AllMatching('air'), 'seasons'])
    baked_df = step.prepare(data).bake(data)

    assert len(baked_df.columns) == 2
    assert 'aired' in baked_df.columns
    assert 'seasons' in baked_df.columns


def test_select_column_step_must_allow_one_column_name(data):
    """
    Step must subset the correct columns using a single Column name.
    """
    step = SelectColumnsStep(columns='seasons')
    baked_df = step.prepare(data).bake(data)

    assert len(baked_df.columns) == 1
    assert 'seasons' in baked_df.columns


def test_numerical_selectors_on_columns(data):
    """
    Test all_numeric as unique selector
    """
    step = SelectColumnsStep(columns=AllNumeric())
    baked_df = step.prepare(data).bake(data)

    assert len(baked_df.columns) == 2
    assert 'year' in baked_df.columns
    assert 'rating' in baked_df.columns


def test_select_columns_step_must_fail_if_column_doesnot_exist_on_df(data):
    """
    Raise an exception if any column does not exist
    """
    with pytest.raises(YeastValidationError):
        step = SelectColumnsStep(columns=['seasons', 'not_found'])
        step.prepare(data).bake(data)


def test_regex_selectors_on_columns(data):
    """
    Test all_numeric
    """
    step = SelectColumnsStep(columns=AllMatching('^sea'))
    baked_df = step.prepare(data).bake(data)

    assert len(baked_df.columns) == 1
    assert 'seasons' in baked_df.columns
