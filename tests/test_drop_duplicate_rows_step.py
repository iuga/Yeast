import pytest
import pandas as pd

from yeast.steps.drop_duplicate_rows_step import DropDuplicateRowsStep
from yeast.errors import YeastValidationError

from data_samples import startrek_data as data


def test_drop_duplicates_based_single_column_keeping_first(data):
    """
    There are 3 series with 7 seasons, keep the first one
    """
    step = DropDuplicateRowsStep(['seasons'])
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 4
    assert baked_df.iloc[0]['seasons'] == 1
    assert baked_df.iloc[1]['seasons'] == 7
    assert baked_df.iloc[1]['title'] == 'TNG'
    assert baked_df.iloc[2]['seasons'] == 4
    assert baked_df.iloc[3]['seasons'] == 2


def test_drop_duplicates_based_single_column_keeping_last(data):
    """
    There are 3 series with 7 seasons, keep the last one
    """
    step = DropDuplicateRowsStep(['seasons'], keep='last')
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 4
    assert baked_df.iloc[0]['seasons'] == 1
    assert baked_df.iloc[1]['seasons'] == 4
    assert baked_df.iloc[2]['seasons'] == 7
    assert baked_df.iloc[2]['title'] == 'Deep Space Nine'
    assert baked_df.iloc[3]['seasons'] == 2


def test_drop_duplicates_based_single_column_removing_all_of_them(data):
    """
    There are 3 series with 7 seasons, remove all duplicates
    """
    step = DropDuplicateRowsStep(['seasons'], keep='none')
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 3
    assert baked_df.iloc[0]['seasons'] == 1
    assert baked_df.iloc[1]['seasons'] == 4
    assert baked_df.iloc[2]['seasons'] == 2


def test_drop_duplicates_based_two_columns(data):
    """
    There are 3 series with 7 seasons, two watched, remove the first one
    """
    step = DropDuplicateRowsStep(['seasons', 'watched'])
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 5
    assert baked_df.iloc[0]['seasons'] == 1
    assert baked_df.iloc[1]['seasons'] == 7
    assert baked_df.iloc[1]['watched'] == True
    assert baked_df.iloc[2]['seasons'] == 4
    assert baked_df.iloc[3]['seasons'] == 7
    assert baked_df.iloc[3]['watched'] == False
    assert baked_df.iloc[4]['seasons'] == 2


def test_drop_duplicates_based_on_all_columns(data):
    """
    Deduplicate based on all columns, there are no matches
    """
    step = DropDuplicateRowsStep()
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 6


def test_drop_duplicates_step_must_fail_if_column_doesnot_exist_on_df(data):
    """
    Raise an exception if any column does not exist
    """
    with pytest.raises(YeastValidationError):
        step = DropDuplicateRowsStep(['seasons', 'not_found'])
        step.prepare(data).bake(data)
