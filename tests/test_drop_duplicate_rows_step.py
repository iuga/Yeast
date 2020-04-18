import pytest
import pandas as pd

from yeast.steps.drop_duplicate_rows_step import DropDuplicateRowsStep

from data_samples import startrek_data as data


def test_xxxx(data):
    step = FilterRowsStep("rating > 9")
    baked_df = step.prepare(data).bake(data)

    assert baked_df.shape[0] == 2
    assert baked_df.iloc[0]['title'] == 'Picard'
    assert baked_df.iloc[1]['title'] == 'TNG'
