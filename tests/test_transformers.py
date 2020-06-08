import numpy as np
import pandas as pd

from yeast.transformers import StrToLower, StrToUpper, StrToSentence, StrToTitle, StrTrim
from yeast.transformers import StrSlice, StrReplace, StrRemove, StrRemoveAll, MapValues
from yeast.transformers import DateYear, DateMonth, DateQuarter, DateWeek, DateDay, DateDayOfWeek
from yeast.transformers import DateHour, DateMinute, DateSecond, DateDayOfYear
from yeast.transformers import Round, Ceil, Floor

from data_samples import startrek_data as data
from data_samples import startrek_characters as chars_data
from data_samples import release_dates


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


def test_str_map_values(chars_data):
    ranks = MapValues({
        'Capitain': 'Captain',
        'CAPTAIN': 'Captain',
        'Comander': 'Commander'
    }).resolve(chars_data, column='rank').to_list()
    assert 'Captain' in ranks
    assert 'Capitain' not in ranks
    assert 'CAPTAIN' not in ranks
    assert 'Commander' in ranks
    assert 'Comander' not in ranks


def test_numerical_map_values(data):
    seasons = MapValues({
        7: 8,
        4: np.NaN
    }).resolve(data, column='seasons').to_list()
    assert seasons[0] == 1
    assert seasons[1] == 8
    assert seasons[2] == 8
    assert np.isnan(seasons[3])
    assert seasons[4] == 8
    assert seasons[5] == 2


def test_extract_date_year(release_dates):
    years = DateYear().resolve(release_dates, column='released').to_list()
    # [1966, 1987, 1993, 1995, 2001, 2017, 2020, <NA>]
    assert years[0] == 1966
    assert years[1] == 1987
    assert years[2] == 1993
    assert years[3] == 1995
    assert years[4] == 2001
    assert years[5] == 2017
    assert years[6] == 2020
    assert pd.isna(years[7])


def test_extract_date_month(release_dates):
    feature = DateMonth().resolve(release_dates, column='released').to_list()
    # [9, 9, 1, 1, 9, 9, 1, <NA>]
    assert feature[0] == 9
    assert feature[1] == 9
    assert feature[2] == 1
    assert feature[3] == 1
    assert feature[4] == 9
    assert feature[5] == 9
    assert feature[6] == 1
    assert pd.isna(feature[7])


def test_extract_date_quarter(release_dates):
    feature = DateQuarter().resolve(release_dates, column='released').to_list()
    # [3, 3, 1, 1, 3, 3, 1, <NA>]
    assert feature[0] == 3
    assert feature[1] == 3
    assert feature[2] == 1
    assert feature[3] == 1
    assert feature[4] == 3
    assert feature[5] == 3
    assert feature[6] == 1
    assert pd.isna(feature[7])


def test_extract_date_week(release_dates):
    feature = DateWeek().resolve(release_dates, column='released').to_list()
    # [36, 40, 53, 3, 39, 38, 4, <NA>]
    assert feature[0] == 36
    assert feature[1] == 40
    assert feature[2] == 53
    assert feature[3] == 3
    assert feature[4] == 39
    assert feature[5] == 38
    assert feature[6] == 4
    assert pd.isna(feature[7])


def test_extract_date_day(release_dates):
    feature = DateDay().resolve(release_dates, column='released').to_list()
    # [8, 28, 3, 16, 26, 24, 23, <NA>]
    assert feature[0] == 8
    assert feature[1] == 28
    assert feature[2] == 3
    assert feature[3] == 16
    assert feature[4] == 26
    assert feature[5] == 24
    assert feature[6] == 23
    assert pd.isna(feature[7])


def test_extract_date_dow(release_dates):
    feature = DateDayOfWeek().resolve(release_dates, column='released').to_list()
    # [3, 0, 6, 0, 2, 6, 3, <NA>]
    assert feature[0] == 3
    assert feature[1] == 0
    assert feature[2] == 6
    assert feature[3] == 0
    assert feature[4] == 2
    assert feature[5] == 6
    assert feature[6] == 3
    assert pd.isna(feature[7])


def test_extract_date_doy(release_dates):
    feature = DateDayOfYear().resolve(release_dates, column='released').to_list()
    # [251, 271, 3, 16, 269, 267, 23, <NA>]
    assert feature[0] == 251
    assert feature[1] == 271
    assert feature[2] == 3
    assert feature[3] == 16
    assert feature[4] == 269
    assert feature[5] == 267
    assert feature[6] == 23
    assert pd.isna(feature[7])


def test_extract_date_hour(release_dates):
    feature = DateHour().resolve(release_dates, column='released').to_list()
    # [0, 0, 12, 0, 13, 0, 15, <NA>]
    assert feature[0] == 0
    assert feature[1] == 0
    assert feature[2] == 12
    assert feature[3] == 0
    assert feature[4] == 13
    assert feature[5] == 0
    assert feature[6] == 15
    assert pd.isna(feature[7])


def test_extract_date_minute(release_dates):
    feature = DateMinute().resolve(release_dates, column='released').to_list()
    # [0, 0, 15, 0, 53, 0, 0, <NA>]
    assert feature[0] == 0
    assert feature[1] == 0
    assert feature[2] == 15
    assert feature[3] == 0
    assert feature[4] == 53
    assert feature[5] == 0
    assert feature[6] == 0
    assert pd.isna(feature[7])


def test_extract_date_seconds(release_dates):
    feature = DateSecond().resolve(release_dates, column='released').to_list()
    # [0, 0, 15, 0, 53, 0, 0, <NA>]
    assert feature[0] == 0
    assert feature[1] == 0
    assert feature[2] == 23
    assert feature[3] == 0
    assert feature[4] == 0
    assert feature[5] == 0
    assert feature[6] == 0
    assert pd.isna(feature[7])


def test_numerical_round(data):
    # [9.3, 9.9, 7.4, 6.8, 8.9, 9.0]
    ratings = Round(digits=0, column='rating').resolve(data).to_list()
    assert ratings[0] == 9
    assert ratings[1] == 10
    assert ratings[2] == 7
    assert ratings[3] == 7
    assert ratings[4] == 9
    assert ratings[5] == 9


def test_numerical_ceil(data):
    # [9.3, 9.9, 7.4, 6.8, 8.9, 9.0]
    ratings = Ceil(column='rating').resolve(data).to_list()
    assert ratings[0] == 10
    assert ratings[1] == 10
    assert ratings[2] == 8
    assert ratings[3] == 7
    assert ratings[4] == 9
    assert ratings[5] == 9


def test_numerical_floor(data):
    # [9.3, 9.9, 7.4, 6.8, 8.9, 9.0]
    ratings = Floor(column='rating').resolve(data).to_list()
    assert ratings[0] == 9
    assert ratings[1] == 9
    assert ratings[2] == 7
    assert ratings[3] == 6
    assert ratings[4] == 8
    assert ratings[5] == 9
