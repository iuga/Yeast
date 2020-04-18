from yeast.steps.sort_rows_step import SortRowsStep

from data_samples import startrek_data as data


def test_sort_rows_by_one_column(data):
    """
    Sort rows by one column
    """
    step = SortRowsStep(columns=['year'])
    baked_df = step.prepare(data).bake(data)

    assert baked_df['year'][0] == 1987
    assert baked_df['year'][1] == 1993
    assert baked_df['year'][2] == 1995
    assert baked_df['year'][3] == 2001
    assert baked_df['year'][4] == 2017
    assert baked_df['year'][5] == 2020

    assert baked_df['title'][0] == 'TNG'
    assert baked_df['title'][1] == 'Deep Space Nine'
    assert baked_df['title'][2] == 'Voyager'
    assert baked_df['title'][3] == 'Enterprise'
    assert baked_df['title'][4] == 'Discovery'
    assert baked_df['title'][5] == 'Picard'


def test_sort_rows_by_two_columns(data):
    """
    Sort rows by two columns and descending (!ascending)
    """
    step = SortRowsStep(columns=['watched', 'rating'], ascending=False)
    baked_df = step.prepare(data).bake(data)

    assert baked_df['watched'][0] == True
    assert baked_df['watched'][1] == True
    assert baked_df['watched'][2] == True
    assert baked_df['watched'][3] == True
    assert baked_df['watched'][4] == False
    assert baked_df['watched'][5] == False

    assert baked_df['rating'][0] == 9.9
    assert baked_df['rating'][1] == 9.0
    assert baked_df['rating'][2] == 7.4
    assert baked_df['rating'][3] == 6.8
    assert baked_df['rating'][4] == 9.3
    assert baked_df['rating'][5] == 8.9
