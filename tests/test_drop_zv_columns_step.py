import pytest
from yeast.steps import DropZVColumnsStep
from yeast.errors import YeastBakeError
from data_samples import release_dates as data


def test_drop_zero_variance_columns_considering_NA_will_not_drop_any_column(data):
    """
    If we consider NA, this df does not contain ZV columns
    """
    step = DropZVColumnsStep()
    bdf = step.prepare(data).bake(data)

    assert 'name' in bdf.columns
    assert 'released' in bdf.columns
    assert 'episodes' in bdf.columns


def test_drop_zero_variance_columns_omiting_NA_will_drop_a_column(data):
    """
    If we omit NA, this df contains a ZV column "episodes"
    """
    step = DropZVColumnsStep(naomit=True)
    bdf = step.prepare(data).bake(data)

    assert 'name' in bdf.columns
    assert 'released' in bdf.columns
    assert 'episodes' not in bdf.columns


def test_drop_zero_variance_on_subset_columns(data):
    """
    with a subset of columns
    """
    step = DropZVColumnsStep(['name', 'released'], naomit=True)
    bdf = step.prepare(data).bake(data)

    assert 'name' in bdf.columns
    assert 'released' in bdf.columns
    assert 'episodes' in bdf.columns


def test_drop_zero_variance_on_subset_columns_with_zv_removals(data):
    """
    with a subset of columns
    """
    step = DropZVColumnsStep(['released', 'episodes'], naomit=True)
    bdf = step.prepare(data).bake(data)

    assert 'name' in bdf.columns
    assert 'released' in bdf.columns
    assert 'episodes' not in bdf.columns


def test_if_bake_and_not_prepare_should_raise_an_error(data):
    """
    If we are baking without preparation we should have an error
    """
    step = DropZVColumnsStep()

    with pytest.raises(YeastBakeError):
        step.bake(data)
