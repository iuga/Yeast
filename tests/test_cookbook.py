import pytest

from yeast import Cookbook, Recipe
from yeast.errors import YeastCookbookError
from yeast.steps import SortStep, CleanColumnNamesStep, FilterStep

from data_samples import startrek_data as data


# def test_chain_of_recipes_using_the_cookbok(data):
#     """
#     """
#     # Define the cookbook
#     cookbook = Cookbook()
#
#     # Recipe One
#     recipe_one = Recipe([CleanColumnNamesStep('snake')])
#     cookbook.add('one', recipe_one)
#
#     # Recipe Two
#     recipe_two = Recipe([FilterStep('watched == False')])
#     cookbook.add('two', recipe_two)
#
#     # Preparing the Workflow
#     cookbook >> cookbook.get('one') >> cookbook.get('two')
#
#     # Execute the cookbook
#     bdf = cookbook.bake(data)


def test_add_recipe_by_name(data):
    """
    Add a new recipe into the cookbook
    """
    # Define the cookbook
    cookbook = Cookbook()
    assert len(cookbook.list()) == 0

    # Define a Recipe
    recipe = Recipe([])

    # Add the Recipe into the Cookbook
    cookbook.add('test.recipe', recipe)
    assert len(cookbook.list()) == 1
    assert 'test.recipe' in cookbook.list()

    # Get the Recipe
    assert cookbook.get('test.recipe') == recipe


def test_adding_two_recipes_with_same_name_raises_an_error(data):
    """
    You can't have two recipes with the same name
    """
    cookbook = Cookbook()
    assert len(cookbook.list()) == 0

    # Define a Recipe
    recipe = Recipe([])

    # Add the Recipe into the Cookbook
    cookbook.add('test.recipe', recipe)
    assert len(cookbook.list()) == 1

    with pytest.raises(YeastCookbookError):
        # Add the seconds Recipe into the Cookbook
        cookbook.add('test.recipe', recipe)

    assert len(cookbook.list()) == 1


def test_get_recipe_does_not_exist_raises_an_error(data):
    """
    You can't get a recipe that was not added before
    """
    cookbook = Cookbook()

    with pytest.raises(YeastCookbookError):
        cookbook.get('test.recipe')
