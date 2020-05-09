import pytest
from yeast import Recipe
from yeast.steps.mutate_step import MutateStep
from yeast.steps.sort_rows_step import SortStep
from yeast.steps.group_by_step import GroupByStep
from yeast.errors import YeastValidationError, YeastBakeError, YeastTransformerError
from yeast.transformers import StrToLower, StrReplace, RowNumber
from data_samples import startrek_starships_specs as starship_data
from data_samples import startrek_data


def test_mutation_using_lambda_function(starship_data):
    """
    As transformer we are using a Lambda function
    """
    step = MutateStep({
        'description': lambda df: df['uid'] + ': ' + df['warp'].astype(str)
    })
    bdf = step.prepare(starship_data).bake(starship_data)

    assert 'description' in bdf.columns
    assert bdf.loc[0]['description'] == 'NCC-1701: 9.2'


def test_modify_variable_using_lambda_function(starship_data):
    """
    As transformer we are using a Lambda function
    """
    step = MutateStep({
        'uid': lambda df: df['uid'] + ': ' + df['warp'].astype(str)
    })
    bdf = step.prepare(starship_data).bake(starship_data)

    assert 'uid' in bdf.columns
    assert len(bdf.columns) == 2
    assert bdf.loc[0]['uid'] == 'NCC-1701: 9.2'


def test_mutation_using_a_transformer(starship_data):
    """
    As transformer we are using a Yeast transformer to create a new variable
    """
    step = MutateStep({
        'lower_uid': StrToLower('uid')
    })
    bdf = step.prepare(starship_data).bake(starship_data)

    assert 'lower_uid' in bdf.columns
    assert bdf.loc[0]['lower_uid'] == 'ncc-1701'


def test_modify_variable_using_a_transformer(starship_data):
    """
    As transformer we are using a Yeast transformer to modify an existen variable
    """
    step = MutateStep({
        'uid': StrToLower('uid')
    })
    bdf = step.prepare(starship_data).bake(starship_data)

    assert 'uid' in bdf.columns
    assert len(bdf.columns) == 2
    assert bdf.loc[0]['uid'] == 'ncc-1701'


def test_if_the_column_was_not_defined_use_the_destination_column(starship_data):
    """
    Both expressions should produce the same result:
    'uid': StrToLower('uid')
    and
    'uid': StrToLower()
    """
    step = MutateStep({
        'uid': StrToLower()
    })
    bdf = step.bake(starship_data)

    assert 'uid' in bdf.columns
    assert len(bdf.columns) == 2
    assert bdf.loc[0]['uid'] == 'ncc-1701'


def test_mutation_using_custom_function(starship_data):
    """
    As transformer we are using a custom function
    """
    def my_step(df):
        return df['uid'] + ': ' + df['warp'].astype(str)

    step = MutateStep({
        'description': my_step
    })

    bdf = step.bake(starship_data)

    assert 'description' in bdf.columns
    assert bdf.loc[0]['description'] == 'NCC-1701: 9.2'


def test_mutation_using_a_transformer_must_follow_the_order(starship_data):
    """
    The execution of mutate must follow the order on the list
    """
    step = MutateStep({
        'uid': [
            StrReplace('N', 'X', column='uid'),
            StrToLower('uid')
        ]
    })
    bdf = step.prepare(starship_data).bake(starship_data)

    assert 'uid' in bdf.columns
    assert len(bdf.columns) == 2
    assert bdf.loc[0]['uid'] == 'xcc-1701'


def test_mutation_using_a_transformer_must_follow_the_order_with_mixed_types(starship_data):
    """
    The execution of mutate must follow the order of the list
    """
    step = MutateStep({
        'uid': [
            lambda df: df['uid'].str.replace('NCC', '0', n=1),
            StrReplace('0', '1', 'uid'),
            lambda df: df['uid'].str.replace('1', '2', n=1),
            StrReplace('2', '3', 'uid')
        ]
    })
    bdf = step.bake(starship_data)

    assert 'uid' in bdf.columns
    assert len(bdf.columns) == 2
    assert bdf.loc[0]['uid'] == '3-1701'


def test_the_proper_error_is_raised_if_error_on_lambda_execution(starship_data):
    """
    YeastBakeError should raise if there is an error on the execution
    """
    step = MutateStep({
        'description': lambda df: df['uid'] + ': ' + df['not_found']
    })
    with pytest.raises(YeastBakeError):
        step.prepare(starship_data).bake(starship_data)


def test_rownumber_mutation_using_a_transformer_after_groupby(startrek_data):
    """
    Use Mutate After a GroupBy with a Transformer to create a new column with the row_number
    inside the group:
    ```
                 title  year  row_number
                Picard  2020         1.0
             Discovery  2017         1.0
            Enterprise  2001         1.0
               Voyager  1995         1.0
       Deep Space Nine  1993         2.0
                   TNG  1987         3.0
    ```
    """
    recipe = Recipe([
        GroupByStep('seasons'),
        MutateStep({
            'row_number': RowNumber('rating')
        }),
        SortStep(['seasons', 'row_number'])
    ])
    bdf = recipe.bake(startrek_data)

    assert bdf[['seasons', 'row_number']].loc[0]['seasons'] == 1
    assert bdf[['seasons', 'row_number']].loc[0]['row_number'] == 1

    assert bdf[['seasons', 'row_number']].loc[1]['seasons'] == 2
    assert bdf[['seasons', 'row_number']].loc[1]['row_number'] == 1

    assert bdf[['seasons', 'row_number']].loc[2]['seasons'] == 4
    assert bdf[['seasons', 'row_number']].loc[2]['row_number'] == 1

    assert bdf[['seasons', 'row_number']].loc[3]['seasons'] == 7
    assert bdf[['seasons', 'row_number']].loc[3]['row_number'] == 1

    assert bdf[['seasons', 'row_number']].loc[4]['seasons'] == 7
    assert bdf[['seasons', 'row_number']].loc[4]['row_number'] == 2

    assert bdf[['seasons', 'row_number']].loc[5]['seasons'] == 7
    assert bdf[['seasons', 'row_number']].loc[5]['row_number'] == 3


def test_rownumber_mutation_using_a_transformer_on_dataframe(startrek_data):
    """
    Test a Rank operation without group by:
    ```
                 title  year  row_number
                   TNG  1987         1.0
       Deep Space Nine  1993         2.0
               Voyager  1995         3.0
            Enterprise  2001         4.0
             Discovery  2017         5.0
                Picard  2020         6.0
    ```
    """
    recipe = Recipe([
        MutateStep({
            'row_number': RowNumber('year')
        }),
        SortStep('year')
    ])
    bdf = recipe.bake(startrek_data)

    assert bdf[['year', 'row_number']].loc[0]['year'] == 1987
    assert bdf[['year', 'row_number']].loc[0]['row_number'] == 1

    assert bdf[['year', 'row_number']].loc[1]['year'] == 1993
    assert bdf[['year', 'row_number']].loc[1]['row_number'] == 2

    assert bdf[['year', 'row_number']].loc[2]['year'] == 1995
    assert bdf[['year', 'row_number']].loc[2]['row_number'] == 3

    assert bdf[['year', 'row_number']].loc[3]['year'] == 2001
    assert bdf[['year', 'row_number']].loc[3]['row_number'] == 4

    assert bdf[['year', 'row_number']].loc[4]['year'] == 2017
    assert bdf[['year', 'row_number']].loc[4]['row_number'] == 5

    assert bdf[['year', 'row_number']].loc[5]['year'] == 2020
    assert bdf[['year', 'row_number']].loc[5]['row_number'] == 6


def test_rownumber_mutation_using_a_lambda_after_groupby(startrek_data):
    """
    Use Mutate After a GroupBy with a lambda to create a new column with the row_number
    inside the group:
    ```
                 title  year  row_number
                Picard  2020         1.0
             Discovery  2017         1.0
            Enterprise  2001         1.0
               Voyager  1995         1.0
       Deep Space Nine  1993         2.0
                   TNG  1987         3.0
    ```
    """
    recipe = Recipe([
        GroupByStep('seasons'),
        MutateStep({
            'row_number': lambda df: df['rating'].rank(method="first")
        }),
        SortStep(['seasons', 'row_number'])
    ])
    bdf = recipe.bake(startrek_data)

    assert bdf[['seasons', 'row_number']].loc[0]['seasons'] == 1
    assert bdf[['seasons', 'row_number']].loc[0]['row_number'] == 1

    assert bdf[['seasons', 'row_number']].loc[1]['seasons'] == 2
    assert bdf[['seasons', 'row_number']].loc[1]['row_number'] == 1

    assert bdf[['seasons', 'row_number']].loc[2]['seasons'] == 4
    assert bdf[['seasons', 'row_number']].loc[2]['row_number'] == 1

    assert bdf[['seasons', 'row_number']].loc[3]['seasons'] == 7
    assert bdf[['seasons', 'row_number']].loc[3]['row_number'] == 1

    assert bdf[['seasons', 'row_number']].loc[4]['seasons'] == 7
    assert bdf[['seasons', 'row_number']].loc[4]['row_number'] == 2

    assert bdf[['seasons', 'row_number']].loc[5]['seasons'] == 7
    assert bdf[['seasons', 'row_number']].loc[5]['row_number'] == 3
