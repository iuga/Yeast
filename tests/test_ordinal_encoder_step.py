import pandas as pd
import pytest
import numpy as np

from yeast.steps.ordinal_encoder_step import OrdinalEncoderStep
from yeast.errors import YeastValidationError

from data_samples import startrek_characters


def test_ordinal_score_on_a_string_column_without_nulls_or_na(startrek_characters):
    """
    Normal flow without NA or None Values
    """
    step = OrdinalEncoderStep(['rank'])
    bdf = step.prepare(startrek_characters).bake(startrek_characters)

    # Mapping:
    # [2, 3, 3, 4, 5, 1, 2, 0]
    ordinal_ranks = bdf['rank'].tolist()
    assert ordinal_ranks[0] == 2  # Captain
    assert ordinal_ranks[1] == 3  # Comander
    assert ordinal_ranks[2] == 3  # Comander
    assert ordinal_ranks[3] == 4  # LT Commander
    assert ordinal_ranks[4] == 5  # None
    assert ordinal_ranks[5] == 1  # Capitain
    assert ordinal_ranks[6] == 2  # Captain
    assert ordinal_ranks[7] == 0  # CAPTAIN


def test_ordinal_score_on_a_string_column_with_nulls_or_na(startrek_characters):
    """
    Normal flow without NA or None Values
    """
    startrek_characters.loc[3, 'rank'] = np.nan
    startrek_characters.loc[7, 'rank'] = None
    step = OrdinalEncoderStep(['rank'])
    bdf = step.prepare(startrek_characters).bake(startrek_characters)

    # Mapping:
    # [1, 2, 2, <NA>, 3, 0, 1, <NA>]
    ordinal_ranks = bdf['rank'].tolist()
    assert ordinal_ranks[0] == 1  # Captain
    assert ordinal_ranks[1] == 2  # Comander
    assert ordinal_ranks[2] == 2  # Comander
    assert pd.isna(ordinal_ranks[3])  # np.nan
    assert ordinal_ranks[4] == 3  # None
    assert ordinal_ranks[5] == 0  # Capitain
    assert ordinal_ranks[6] == 1  # Captain
    assert pd.isna(ordinal_ranks[7])  # None


def test_ordinal_score_on_columns_doesnot_exist_should_raise_an_error(startrek_characters):
    """
    Raise an error, "not_found" column does not exist
    """
    step = OrdinalEncoderStep('not_found')

    with pytest.raises(YeastValidationError):
        step.prepare(startrek_characters)
