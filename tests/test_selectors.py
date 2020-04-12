import pytest
import pandas as pd
from yeast.steps.select_columns_step import SelectColumnStep
from yeast.errors import YeastValidationError
from yeast.selectors import AllNumeric, AllMatching, AllString, AllMatching, AllBoolean
from yeast.selectors import AllDatetime, AllCategorical, AllColumns


@pytest.fixture
def data():
    pdf = pd.DataFrame({
        'title': ['Picard', 'TNG', 'Voyager', 'Enterprise', 'Deep Space Nine', 'Discovery'],
        'year': [2020, 1987, 1995, 2001, 1993, 2017],
        'seasons': [1, 7, 7, 4, 7, 2],
        'watched': [False, True, True, True, False, True],
        'rating': [9.3, 9.9,7.4, 6.8, 8.9, 9.0],
        'aired': ['20200203', '19870612', '19950101', '20011231', '19930102', '20170524']
    })
    pdf['title'] = pdf['title'].astype('string')
    pdf['seasons'] = pdf['seasons'].astype('category')
    pdf['aired'] = pd.to_datetime(pdf['aired'])
    return pdf


def test_select_all_columns(data):
    """
    Select all columns
    """
    columns = AllColumns().resolve(data)

    assert 'year' in columns
    assert 'rating' in columns
    assert 'seasons' in columns
    assert 'watched' in columns
    assert 'title' in columns
    assert 'aired' in columns


def test_select_all_numerical(data):
    """
    Select all numerical columns
    """
    columns = AllNumeric().resolve(data)

    assert 'year' in columns
    assert 'rating' in columns

    assert 'seasons' not in columns
    assert 'watched' not in columns
    assert 'title' not in columns
    assert 'aired' not in columns


def test_select_all_strings(data):
    """
    Select all string columns
    """
    columns = AllString().resolve(data)

    assert 'title' in columns

    assert 'seasons' not in columns
    assert 'rating' not in columns
    assert 'watched' not in columns
    assert 'year' not in columns
    assert 'aired' not in columns


def test_select_all_matching(data):
    """
    Select all string columns
    """
    columns = AllMatching('ed$').resolve(data)

    assert 'watched' in columns
    assert 'aired' in columns

    assert 'title' not in columns
    assert 'seasons' not in columns
    assert 'year' not in columns
    assert 'rating' not in columns


def test_select_all_boolean(data):
    """
    Select all boolean columns
    """
    columns = AllBoolean().resolve(data)

    assert 'watched' in columns

    assert 'seasons' not in columns
    assert 'rating' not in columns
    assert 'title' not in columns
    assert 'year' not in columns
    assert 'aired' not in columns


def test_select_all_datetime(data):
    """
    Select all datetime columns
    """
    columns = AllDatetime().resolve(data)

    assert 'aired' in columns

    assert 'seasons' not in columns
    assert 'rating' not in columns
    assert 'title' not in columns
    assert 'year' not in columns
    assert 'watched' not in columns



def test_select_all_categorical(data):
    """
    Select all categorical columns
    """
    columns = AllCategorical().resolve(data)

    assert 'seasons' in columns

    assert 'aired' not in columns
    assert 'rating' not in columns
    assert 'title' not in columns
    assert 'year' not in columns
    assert 'watched' not in columns
