import pytest
import pandas as pd
from yeast.steps.select_columns_step import SelectColumnStep
from yeast.errors import YeastValidationError


@pytest.fixture
def data():
    return pd.DataFrame({
        'title': ['Picard', 'TNG', 'Voyager', 'Enterprise', 'Deep Space Nine', 'Discovery'],
        'year': [2020, 1987, 1995, 2001, 1993, 2017],
        'seasons': [1, 7, 7, 4, 7, 2]
    })


def test_select_column_step_must_subset_columns(data):
    """
    Step must subset the correct columns from the df
    """
    step = SelectColumnStep(columns=['year', 'seasons'])
    baked_df = step.prepare(data).bake(data)
    assert 'year' in baked_df.columns
    assert 'seasons' in baked_df.columns
    assert 'title' not in baked_df.columns


def test_select_columns_step_must_fail_if_column_doesnot_exist_on_df(data):
    """
    Raise an exception if any column does not exist
    """
    with pytest.raises(YeastValidationError):
        step = SelectColumnStep(columns=['seasons', 'not_found'])
        step.prepare(data).bake(data)


def test_select_columns_step_must_fail_if_column_is_not_string(data):
    """
    Raise an exception if any column is not string
    """
    with pytest.raises(YeastValidationError):
        step = SelectColumnStep(columns=[42, 'not_found'])
        step.prepare(data).bake(data)
