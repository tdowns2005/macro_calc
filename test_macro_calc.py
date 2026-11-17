"""
Test Macro Calc by Travis Downs
Purpose: This program tests the functions and error catches in the Macro Calc
         application
Completed: 26/10/2026 
"""


from pathlib import Path

import pytest
from pytest import approx

# Imports path, pytest, and approx

from macro_calc import (
    CALORIE_INDEX,
    CATEGORY_INDEX,
    FOOD_NAME_INDEX,
    calc_totals,
    find_foods,
    portion_calc,
    read_dictionary,
)
#Imports functions and indexes from macro calc


def test_read_dictionary_loads_foods():
    """
    Verify that the food CSV is loaded into a dictionary.
    """
    
    filename = Path(__file__).with_name("foods.csv")

    foods = read_dictionary(filename, FOOD_NAME_INDEX)

    assert "Black beans - boiled without salt" in foods
    assert "Apple with skin - raw" in foods
    assert "Lentils - boiled without salt" in foods
    # Checks for 3 items in the dataset


def test_read_dictionary_stores_the_correct_row():
    """
    Verify that a known food has the expected values.
    """
    
    filename = Path(__file__).with_name("foods.csv")

    foods = read_dictionary(filename, FOOD_NAME_INDEX)
    apple = foods["Apple with skin - raw"]

    assert apple[FOOD_NAME_INDEX] == "Apple with skin - raw"
    assert apple[CATEGORY_INDEX] == "Fruit"
    assert apple[CALORIE_INDEX] == "52"
    # Checks for data integrity by checking food name category and calories of
    # apple



def test_find_foods_ignores_case():
    """
    Verify that food searches are not case-sensitive.
    """
    
    foods = {
        "Test Apple": ["Test Apple", "Fruit", "100", "50", "1",
                       "10", "5", "0", "1", "0"],
        "TEST BANANA": ["Test Banana", "Fruit", "100", "50", "1",
                       "10", "5", "0", "1", "0"],
        "tesT blacK beanS": ["Test Black Beans", "Legume", "100", "50", "1",
                       "10", "5", "0", "1", "0"]
    }

    matches = find_foods("apple", foods)
    assert "Test Apple" in matches

    matches = find_foods("banana", foods)
    assert "TEST BANANA" in matches

    matches = find_foods("black beans", foods)
    assert "tesT blacK beanS" in matches

    # Checks that searches are not case sensitive using apple banana and black
    # beans, all with different capatalization 


def test_find_foods_returns_match():
    """
    Verify that a search will return zero, one, or multiple matches
    """
    foods = {
        "Apple": ["Apple"],
        "Apple juice": ["Apple juice"],
        "Apple pie": ["Apple pie"]
    }

    empty_matches = find_foods("unknown", foods)
    assert empty_matches == {}
    # Checks for no matches

    one_match = find_foods("juice", foods)
    assert len(one_match) == 1
    assert "Apple juice" in one_match
    # Checks for one match

    three_matches = find_foods("apple", foods)
    assert len(three_matches) == 3
    # Checks for three matches

def test_portion_calc_for_150_grams():
    """
    Verify that nutrients are scaled up by portion multiplier
    """
    
    food = ["Test food", "Test", "100", "200", "10",
            "20", "5", "1", "8", "2"]
    

    result = portion_calc(food, 150)
    # Creates a multiplier of 1.5

    assert result["calories"] == approx(300)
    assert result["protein"] == approx(15)
    assert result["carbohydrates"] == approx(30)
    assert result["total_sugars"] == approx(7.5)
    assert result["added_sugars"] == approx(1.5)
    assert result["fat"] == approx(12)
    assert result["saturated_fat"] == approx(3)
    # Fictional food macronutrients scaled up by 1.5



def test_calc_totals_adds_portions():
    """Verify that multiple portions are added together."""
    portions = [
        {
            "calories": 100,
            "protein": 5,
            "carbohydrates": 10,
            "total_sugars": 4,
            "added_sugars": 1,
            "fat": 2,
            "saturated_fat": 1
        },
        {
            "calories": 200,
            "protein": 10,
            "carbohydrates": 20,
            "total_sugars": 8,
            "added_sugars": 2,
            "fat": 4,
            "saturated_fat": 2
        }
    ]

    totals = calc_totals(portions)

    assert totals["calories"] == approx(300)
    assert totals["protein"] == approx(15)
    assert totals["carbohydrates"] == approx(30)
    assert totals["total_sugars"] == approx(12)
    assert totals["fat"] == approx(6)
    # Checks that macronutrients are added properly

pytest.main(["-v", "--tb=line", "-rN", __file__])
