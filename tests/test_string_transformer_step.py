import pytest

from yeast.steps.string_transform_step import StringTransformStep
from yeast.errors import YeastValidationError
from yeast.transformers import StrToTitle, StrToLower, StrTrim, StrReplace, StrReplaceAll

from data_samples import startrek_data as data
from data_samples import startrek_characters as chars_data


def test_basic_usage_of_string_transform_step(data):
    """
    We are only going to lower a column
    """
    step = StringTransformStep(columns=['title'], transformers=[
        StrToLower()
    ])
    baked_df = step.prepare(data).bake(data)

    titles = baked_df['title'].to_list()
    assert 'picard' in titles
    assert 'tng' in titles
    assert 'voyager' in titles
    assert 'enterprise' in titles
    assert 'deep space nine' in titles
    assert 'discovery' in titles


def test_string_transformation_workflow_on_name_column(chars_data):
    """
    Apply some transformations to the columns:
    - String to Sentence
    """
    step = StringTransformStep(columns=['name'], transformers=[
        # "JONATHAN ARCHER" to "Jonathan Archer"
        StrToTitle(),
        # " Data " to "Data"
        StrTrim(),
        # "Philippa  Georgiou" to "Philippa Georgiou"
        StrReplace('  ', ' '),
        # "Jean--Luc PICARD" to "Jean-Luc Picard"
        StrReplaceAll('--', '-')
    ])
    baked_df = step.prepare(chars_data).bake(chars_data)

    names = baked_df['name'].to_list()
    assert "Jonathan Archer" in names
    assert 'Data' in names
    assert 'Philippa Georgiou' in names
    assert 'Jean-Luc Picard' in names


def test_string_transformation_workflow_on_rank_column(chars_data):
    """
    Apply some transformations to the columns:
    - String to Sentence
    """
    step = StringTransformStep(columns=['rank'], transformers=[
        # "LT Commander" to "Lt Commander"
        StrToTitle(),
        # "Comander" to "Commander"
        StrReplace("Comander", "Commander"),
        # "Capitain" to "Captain"
        StrReplace("Capitain", "Captain"),
        # "Lt Commander" to "Lt. Commander"
        StrReplace("Lt", "Lt."),
        # "None" to "Chief Medical Officer"
        StrReplace("None", "Chief Medical Officer")
    ])
    baked_df = step.prepare(chars_data).bake(chars_data)

    names = sorted(set(baked_df['rank'].to_list()))
    assert len(names) == 4
    assert names[0] == 'Captain'
    assert names[1] == 'Chief Medical Officer'
    assert names[2] == 'Commander'
    assert names[3] == 'Lt. Commander'
