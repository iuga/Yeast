import pytest

from yeast.steps.custom_step import CustomStep
from yeast.errors import YeastValidationError

from data_samples import startrek_characters as chars_data


def test_custom_bake_method(chars_data):
    """
    Tru only a custom bake method
    """
    def concatenate_name_rank(step, df):
        df['full_name'] = df['name'] + ' - ' + df['rank']
        return df

    step = CustomStep(to_bake=concatenate_name_rank)
    baked_df = step.prepare(chars_data).bake(chars_data)

    assert baked_df.shape == (8, 3)
    assert baked_df['full_name'][1] == 'Michael Burnham - Comander'


def test_custom_validate_method(chars_data):
    """
    Test a custom validation and fail it raising a YeastValidationError
    """
    def validate_columns_but_fail(step, df):
        if 'age' not in df.columns:
            raise YeastValidationError('Age not found')

    step = CustomStep(to_validate=validate_columns_but_fail)

    with pytest.raises(YeastValidationError):
        step.prepare(chars_data).bake(chars_data)


def test_custom_prepare_and_bake_method(chars_data):
    """
    Let's generate some data on prepare that it's needed on the bake
    """
    def get_name_length(step, df):
        step.name_length = df['name'].str.len().mean()

    def add_name_length(step, df):
        df['length'] = step.name_length
        return df

    step = CustomStep(to_prepare=get_name_length, to_bake=add_name_length)
    baked_df = step.prepare(chars_data).bake(chars_data)

    assert baked_df.shape == (8, 3)
    assert baked_df['name'][1] == 'Michael Burnham'
    assert baked_df['rank'][1] == 'Comander'
    assert baked_df['length'][1] == 13.5


def test_full_inheritance_of_the_custom_step(chars_data):
    """
    Let's create a CustomStep inheriting from CustomStep
    """
    class FullNameStep(CustomStep):

        def do_validate(self, df):
            if 'name' not in df.columns or 'rank' not in df.columns:
                raise YeastValidationError('Name or Rank not found')

        def do_bake(self, df):
            df['full_name'] = df['name'] + ' - ' + df['rank']
            return df

    step = FullNameStep()
    baked_df = step.prepare(chars_data).bake(chars_data)

    assert baked_df.shape == (8, 3)
    assert baked_df['full_name'][1] == 'Michael Burnham - Comander'
