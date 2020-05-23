import pytest
import pandas as pd
import numpy as np


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


@pytest.fixture
def warp_factors():
    """
    Specs of the Star Trek SpaceShips
    """
    pdf = pd.DataFrame({
        'uid': [
            'NCC-1701',
            'Narada',
            'NCC-74656',
            'NCC-1031',
            'NCC-1764',
            'NX-01',
            'Borg cube',
            None,
        ],
        'warp': [
            9.2,
            np.nan,
            9.975,
            9.9,
            9.2,
            4,
            None,
            np.nan
        ]
    })
    return pdf


@pytest.fixture
def release_dates():
    """
    Series Release Dates
    """
    pdf = pd.DataFrame({
        'name': [
            'The Original Series',
            'The Next Generation',
            'Deep Space Nine',
            'Voyager',
            'Enterprise',
            'Discovery',
            'Picard',
            'Strange New Worlds'
        ],
        'released': [
            '1966-09-08',
            '1987-09-28',
            '1993-01-03 12:15:23',
            '1995-01-16',
            '2001-09-26 13:53',
            '2017-09-24',
            '2020-01-23 15',
            np.nan
        ]
    })
    return pdf
