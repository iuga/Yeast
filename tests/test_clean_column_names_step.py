import pytest
import pandas as pd

from yeast import steps, errors


@pytest.fixture
def data():
    return pd.DataFrame({
        'series_Name': ['Picard', 'TNG', 'Voyager', 'Enterprise', 'Deep Space Nine', 'Discovery'],
        'CreationYear': [2020, 1987, 1995, 2001, 1993, 2017],
        'Total Seasons': [1, 7, 7, 4, 7, 2]
    })


def test_snake_case_cleaning(data):
    """
    Test the snake case transformation
    """
    step = steps.CleanColumnNamesStep('snake')
    baked_df = step.prepare(data).bake(data)

    assert 'series_name' in baked_df.columns
    assert 'creation_year' in baked_df.columns
    assert 'total_seasons' in baked_df.columns

    assert 'series_Name' not in baked_df.columns
    assert 'CreationYear' not in baked_df.columns
    assert 'Total Seasons' not in baked_df.columns


def test_upper_camel_case_cleaning(data):
    """
    Test the upper camel case transformation
    """
    step = steps.CleanColumnNamesStep('upper_camel')
    baked_df = step.prepare(data).bake(data)

    assert 'SeriesName' in baked_df.columns
    assert 'CreationYear' in baked_df.columns
    assert 'TotalSeasons' in baked_df.columns

    assert 'series_Name' not in baked_df.columns
    assert 'Total Seasons' not in baked_df.columns


def test_lower_camel_case_cleaning(data):
    """
    Test the lower camel case transformation
    """
    step = steps.CleanColumnNamesStep('lower_camel')
    baked_df = step.prepare(data).bake(data)

    assert 'seriesName' in baked_df.columns
    assert 'creationYear' in baked_df.columns
    assert 'totalSeasons' in baked_df.columns

    assert 'series_Name' not in baked_df.columns
    assert 'CreationYear' not in baked_df.columns
    assert 'Total Seasons' not in baked_df.columns


def test_snake_case_with_whitespaces_before_and_after(data):
    """
    Test cleaning with whitespaces before and after the name
    """
    data.columns = ['   series_Name    ', '  CreationYear', 'Total Seasons  ']
    step = steps.CleanColumnNamesStep('snake')
    baked_df = step.prepare(data).bake(data)

    assert 'series_name' in baked_df.columns
    assert 'creation_year' in baked_df.columns
    assert 'total_seasons' in baked_df.columns


def test_invalid_case_must_raise_error(data):
    """
    Error on invalid case
    """
    with pytest.raises(errors.YeastValidationError):
        step = steps.CleanColumnNamesStep('camel')
        step.prepare(data).bake(data)
