import pytest
import pandas as pd


@pytest.fixture
def startrek_data():
    """
    Sample Data Frame with Star Trek data
    """
    pdf = pd.DataFrame({
        'title': ['Picard', 'TNG', 'Voyager', 'Enterprise', 'Deep Space Nine', 'Discovery'],
        'year': [2020, 1987, 1995, 2001, 1993, 2017],
        'seasons': [1, 7, 7, 4, 7, 2],
        'watched': [False, True, True, True, False, True],
        'rating': [9.3, 9.9, 7.4, 6.8, 8.9, 9.0],
        'aired': ['20200203', '19870612', '19950101', '20011231', '19930102', '20170524']
    })
    pdf['title'] = pdf['title'].astype('string')
    pdf['seasons'] = pdf['seasons'].astype('category')
    pdf['aired'] = pd.to_datetime(pdf['aired'])
    return pdf


@pytest.fixture
def startrek_characters():
    """
    Text dataset of the Star Trek Characters
    """
    pdf = pd.DataFrame({
        'name': [
            'JONATHAN ARCHER',
            'Michael Burnham',
            'Chakotay ',
            '  Data  ',
            'the Doctor',
            'philippa  georgiou',
            'Jean--Luc PICARD',
            'Christopher pike '
        ],
        'rank': [
            'Captain',
            'Comander',
            'Comander',
            'LT Commander',
            'None',
            'Capitain',
            'Captain',
            'CAPTAIN',
        ]
    })
    return pdf
