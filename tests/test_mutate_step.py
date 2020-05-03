import pytest
from yeast.steps.mutate_step import MutateStep
from yeast.steps.sort_rows_step import SortStep
from yeast.errors import YeastValidationError, YeastBakeError, YeastTransformerError
from yeast.transformers import StrToLower, StrReplace
from data_samples import startrek_starships_specs as starship_data


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


def test_mutation_using_custom_function(starship_data):
    """
    As transformer we are using a custom function
    """
    def my_step(df):
        return df['uid'] + ': ' + df['warp'].astype(str)

    step = MutateStep({
        'description': my_step
    })

    import pdb; pdb.set_trace()
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
            StrReplace('2', '3', 'uid'),
            SortStep('uid')
        ]
    })
    bdf = step.prepare(starship_data).bake(starship_data)

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


def test_mutation_using_a_transformer_without_pass_column_name(starship_data):
    """
    Transformer (StrToLower) needs a column name in this context or will fail
    """
    step = MutateStep({
        'lower_uid': StrToLower()
    })
    with pytest.raises(YeastTransformerError):
        step.prepare(starship_data).bake(starship_data)
