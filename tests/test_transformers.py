from yeast.transformers import StrToLower, StrToUpper

from data_samples import startrek_data as data


def test_str_to_lower(data):
    titles = StrToLower().resolve(data['title']).to_list()

    assert 'picard' in titles
    assert 'tng' in titles
    assert 'voyager' in titles
    assert 'enterprise' in titles
    assert 'deep space nine' in titles
    assert 'discovery' in titles


def test_str_to_upper(data):
    titles = StrToUpper().resolve(data['title']).to_list()

    assert 'PICARD' in titles
    assert 'TNG' in titles
    assert 'VOYAGER' in titles
    assert 'ENTERPRISE' in titles
    assert 'DEEP SPACE NINE' in titles
    assert 'DISCOVERY' in titles
