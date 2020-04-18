import pytest

from yeast.steps.rename_columns_step import RenameColumnsStep
from yeast.errors import YeastValidationError

from data_samples import startrek_data as data


def test_a_simple_column_rename(data):
    """
    Let's rename two columns on the DataFrame
    """
    step = RenameColumnsStep({
        'title': 'series_title',
        'aired': 'aired_on'
    })
    baked_df = step.prepare(data).bake(data)

    assert 'series_title' in baked_df.columns
    assert 'aired_on' in baked_df.columns

    assert 'title' not in baked_df.columns
    assert 'aired' not in baked_df.columns


def test_that_the_mapping_olny_accept_string_names(data):
    """
    Other types than string are not supported
    """
    step = RenameColumnsStep({
        'title': 'series_title',
        'aired': ['aired_on']
    })

    with pytest.raises(YeastValidationError):
        baked_df = step.prepare(data).bake(data)
