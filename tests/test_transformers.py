from yeast.transformers import StrToLower, StrToUpper, StrToSentence, StrToTitle, StrTrim
from yeast.transformers import StrSlice, StrReplace, StrRemove, StrRemoveAll

from data_samples import startrek_data as data
from data_samples import startrek_characters as chars_data


def test_str_to_lower(data):
    titles = StrToLower().resolve(data, column='title').to_list()
    assert 'picard' in titles
    assert 'tng' in titles
    assert 'voyager' in titles
    assert 'enterprise' in titles
    assert 'deep space nine' in titles
    assert 'discovery' in titles


def test_str_to_upper(data):
    titles = StrToUpper('title').resolve(data).to_list()
    assert 'PICARD' in titles
    assert 'TNG' in titles
    assert 'VOYAGER' in titles
    assert 'ENTERPRISE' in titles
    assert 'DEEP SPACE NINE' in titles
    assert 'DISCOVERY' in titles


def test_str_to_sentence(chars_data):
    titles = StrToSentence().resolve(chars_data, column='name').to_list()
    assert 'Jonathan archer' in titles
    assert 'Michael burnham' in titles


def test_str_to_title(chars_data):
    titles = StrToTitle('name').resolve(chars_data).to_list()
    assert 'Jonathan Archer' in titles
    assert 'Michael Burnham' in titles


def test_str_trim(chars_data):
    titles = StrTrim().resolve(chars_data, column='name').to_list()
    assert 'Data' in titles


def test_str_slice(chars_data):
    titles = StrSlice(start=0, stop=2).resolve(chars_data, column='name').to_list()
    assert 'JO' in titles


def test_str_replace(chars_data):
    titles = StrReplace('Michael', 'Mike').resolve(chars_data, column='name').to_list()
    assert 'Mike Burnham' in titles


def test_str_remove(chars_data):
    titles = StrRemove('Michael ').resolve(chars_data, column='name').to_list()
    assert 'Burnham' in titles


def test_str_remove_all(chars_data):
    titles = StrRemoveAll('p').resolve(chars_data, column='name').to_list()
    assert 'hilia  georgiou' in titles
