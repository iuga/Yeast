import pytest
import numpy as np

from yeast.steps.replace_na_step import ReplaceNAStep
from yeast.errors import YeastValidationError

from data_samples import warp_factors as data


def test_replace_na_values_on_numerical_data_on_one_column(data):
    """
    Replace NA values on a numerical column, without change other columns
    """
    step = ReplaceNAStep({
        'warp': 1.0
    })
    bdf = step.prepare(data).bake(data)

    assert bdf['warp'].isna().sum() == 0
    assert bdf['warp'].loc[1] == 1.0
    assert bdf['warp'].loc[6] == 1.0
    assert bdf['warp'].loc[7] == 1.0

    assert bdf['uid'].isna().sum() == 1
    assert bdf['uid'].loc[7] is None


def test_replace_na_values_on_categorical_data_on_one_column(data):
    """
    Replace NA values on a categorical column, without change other columns
    """
    step = ReplaceNAStep({
        'uid': 'Unknow'
    })
    bdf = step.prepare(data).bake(data)

    assert bdf['warp'].isna().sum() == 3
    assert np.isnan(bdf['warp'].loc[1])
    assert np.isnan(bdf['warp'].loc[6])
    assert np.isnan(bdf['warp'].loc[7])

    assert bdf['uid'].isna().sum() == 0
    assert bdf['uid'].loc[7] == 'Unknow'


def test_replace_na_values_on_numerical_data_on_one_column_without_mapping(data):
    """
    Replace NA values on a numerical column, without change other columns, directly
    """
    step = ReplaceNAStep('warp', 1.0)
    bdf = step.prepare(data).bake(data)

    assert bdf['warp'].isna().sum() == 0
    assert bdf['warp'].loc[1] == 1.0
    assert bdf['warp'].loc[6] == 1.0
    assert bdf['warp'].loc[7] == 1.0

    assert bdf['uid'].isna().sum() == 1
    assert bdf['uid'].loc[7] is None


def test_if_missing_column_raises_an_error(data):
    """
    For NA replacement all columns must exist
    """
    step = ReplaceNAStep({'not_found': 0, 'not_exist': 1})

    with pytest.raises(YeastValidationError) as ex:
        baked_df = step.prepare(data).bake(data)


def test_if_mapping_in_not_string_or_dict_raises_an_error(data):
    """
    Mapping only supports dict or str
    """
    step = ReplaceNAStep(1, 1)

    with pytest.raises(YeastValidationError) as ex:
        baked_df = step.prepare(data).bake(data)


def test_if_missing_column_on_direct_approach_raises_an_error(data):
    """
    For NA replacement all columns must exist
    """
    step = ReplaceNAStep('not_found', 0)

    with pytest.raises(YeastValidationError) as ex:
        baked_df = step.prepare(data).bake(data)
