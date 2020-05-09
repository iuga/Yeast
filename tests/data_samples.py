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


@pytest.fixture
def startrek_starships():
    """
    Dataset of the Star Trek SpaceShips
    """
    pdf = pd.DataFrame({
        'uid': [
            'NCC-1701',
            'NCC-74656',
            'NCC-1031',
            'NCC-1764',
            'NX-01'
        ],
        'name': [
            'USS Enterprise',
            'USS Voyager',
            'USS Discovery',
            'USS Defiant',
            'Enterprise'
        ]
    })
    return pdf


@pytest.fixture
def startrek_starships_specs():
    """
    Specs of the Star Trek SpaceShips
    """
    pdf = pd.DataFrame({
        'uid': [
            'NCC-1701',
            'NCC-74656',
            'NCC-1031',
            'NCC-1764'
        ],
        'warp': [
            9.2,
            9.975,
            9.9,
            9.2
        ]
    })
    return pdf