import pytest
import pandas as pd

from yeast.steps.filter_rows_step import FilterRowsStep

from data_samples import startrek_data as data


def test_filter_based_on_numeric_variable(data):
    step = FilterRowsStep("rating > 9")
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 2
    assert baked_df.iloc[0]['title'] == 'Picard'
    assert baked_df.iloc[1]['title'] == 'TNG'


def test_filter_based_on_categorical_string_variable(data):
    step = FilterRowsStep("title == 'TNG'")
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 1
    assert baked_df.iloc[0]['title'] == 'TNG'


def test_filter_based_on_two_column_comparison(data):
    step = FilterRowsStep("rating > year")
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 0


def test_query_by_complex_string_match(data):
    """
    Filter by a string on a column
    """
    step = FilterRowsStep("watched == True & seasons == 7")
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 2
    assert baked_df.iloc[0]['title'] == 'TNG'
    assert baked_df.iloc[1]['title'] == 'Voyager'


def test_query_with_in_complex_comparison(data):
    step = FilterRowsStep('watched == True and seasons in [2, 7]')
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 3
    assert baked_df.iloc[0]['title'] == 'TNG'
    assert baked_df.iloc[1]['title'] == 'Voyager'
    assert baked_df.iloc[2]['title'] == 'Discovery'


def test_chaining_of_commands(data):
    step = FilterRowsStep('(watched == True) & (rating >= 7) & (seasons != 2)')
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 2
    assert baked_df.iloc[0]['title'] == 'TNG'
    assert baked_df.iloc[1]['title'] == 'Voyager'
