"""
Macro calc program by Travis Downs
Purpose: This program is to act as a food logger such as my fitness pal 
         or macrofactor. It allows users to enter in the food they consumed
         in a given day. The program will then calculate calories and macronutrients
         based on a food dataset named "foods.csv". Daily totals will be saved
         to a food log where the user can view their macronutrient totals for
         each day

Completed: 26/10/2026
"""

FOOD_NAME_INDEX = 0 
CATEGORY_INDEX = 1 
SERVING_INDEX = 2 
CALORIE_INDEX = 3
PROTEIN_INDEX = 4
CARBOHYDRATE_INDEX = 5
TOTAL_SUGAR_INDEX = 6
ADDED_SUGAR_INDEX = 7
FAT_INDEX = 8
SAT_FAT_INDEX = 9
#Creates indexes for food data

from datetime import datetime
import csv
now = datetime.now(tz=None)
formatted_time = now.strftime("%a %b %d %H:%M:%S %Y")
#Imports csv, and date time and creates a variable for current datetime

def read_dictionary(filename, key_index):
    """
    Reads the food data table and creates a dictionary
    based on the selected key column.

    Parameters:
        filename: name of the CSV file
        key_index: column index used as the dictionary key

    Returns:
        dictionary
    """
    dictionary = {}

    try:
        with open(filename, "rt", newline="") as file:
            reader = csv.reader(file)
            next(reader)  
            # Opens the file and skips the header row

            for row in reader:
                if row:
                    key = row[key_index]
                    dictionary[key] = row
                    # Creates dictionary based on food dataset

    except FileNotFoundError:
        print(f"Error: {filename} not found")
        # Errors out if file cannot be found

    except PermissionError:
        print(f"Error: permission to access {filename} denied")
        # Errors out if user does not have permission to view the file

    return dictionary

def portion_calc(food, serving):
    """
    Calculates the macronutrients of a food based on a given portion

        Parameters: 
        Food: The food with the given nutrients
        Serving: The selected food's serving

        Return: A dictionary of macronutrients in the portion of food consumed 
    """
    
    usr_serving = float(serving)
    food_serving = float(food[SERVING_INDEX])
    # Assigns usr_serving to the amount the user consumed 
    # and food serving to default serving size
    if usr_serving <0 or food_serving <0:
        raise ValueError("Error: servings cannot be negative")
        # Errors out if user or default servings are negative
    else:
        try:
            multiplier = usr_serving / food_serving
            # Creates macronutrient multiplier
        except ZeroDivisionError:
            print("Error: default serving size cannot be zero")
            # Errors out if default serving is zero 

        return {
                "calories": float(food[CALORIE_INDEX]) * multiplier,
                "protein": float(food[PROTEIN_INDEX]) * multiplier,
                "carbohydrates": float(food[CARBOHYDRATE_INDEX]) * multiplier,
                "total_sugars": float(food[TOTAL_SUGAR_INDEX]) * multiplier,
                "added_sugars": float(food[ADDED_SUGAR_INDEX]) * multiplier,
                "fat": float(food[FAT_INDEX]) * multiplier,
                "saturated_fat": float(food[SAT_FAT_INDEX]) * multiplier
                }
        # Returns dictionary of macronutrients in the portion consumed


def add_food(filename):
    """
    Appends user-entered food to the food dataset
        Parameters: 
        Filename: foods.csv
    
        Return: None
    """
    food = input("Enter in the food name: ")
    category = input("Enter the food category: ")
    serving = float(input("How many grams per serving? "))
    calories = float(input("How many calories per serving? "))
    protein = float(input("How many grams of protein per serving? "))
    carbohydrate = float(input("How many grams of carbohydrates per serving? "))
    total_sugar = float(input("How many grams of sugar per serving? "))
    added_sugar = float(input("How many grams of added sugar per serving? "))
    fat = float (input("How many grams of fat per serving? "))
    sat_fat = float(input("How many grams of saturated fat per serving? "))
    # Gathers a series of input from the user about food information

    if any(value < 0 for value in(
        serving,
        calories,
        protein,
        carbohydrate,
        total_sugar,
        added_sugar,
        fat,
        sat_fat
    )) or serving == 0 : 
        raise ValueError("Error: values cannot be negative")
    # Disallows the user to enter any negative inputs or serving size as zero 

    else:
        new_row = [food, category, serving, calories, protein, carbohydrate,
                total_sugar, added_sugar, fat, sat_fat, "user-entered",
                "", ""]
        # Creates a list called new row which will be appended to foods.csv

        
        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
        # Appends new food data to foods.csv

def calc_totals(portions):
    """
    Calculates the total macronutrients based on a full days worth of eating

        Parameters: 
        Portion: A list of macronutrients of the foods the user consumed

        Return: totals
    """
    
    nutrients = [
        "calories",
        "protein",
        "carbohydrates",
        "total_sugars",
        "added_sugars",
        "fat",
        "saturated_fat"
    ]
    # Macronutrient types
    totals = {}

   
    for i in nutrients:
        totals[i] = 0

        for portion in portions:
            totals[i] += portion[i]
    
    return totals

def display_print_totals(totals, logfile):
    """
    Displays the total macronutrient intake for the day and saves it to 
    foodlog.txt

        Parameters: 
        totals: The total amount of macronutrients consumed
        logfile: logfile.txt

        Return: None
    """
    
    lines = [
        f"Calories: {totals['calories']:.2f}",
        f"Protein: {totals['protein']:.2f} g",
        f"Carbohydrates: {totals['carbohydrates']:.2f} g",
        f"Total sugars: {totals['total_sugars']:.2f} g",
        f"Added sugars: {totals['added_sugars']:.2f} g",
        f"Fat: {totals['fat']:.2f} g",
        f"Saturated fat: {totals['saturated_fat']:.2f} g"
    ]
    # Creates a list of formatted strings 
    # which will display each macronutrient total

    print("Total nutrients for the day!")
    print("\n".join(lines))
    input("Press enter to continue: ")
    # Prints the macronutrient total to the terminal


    with open(logfile, "at") as file:
        file.write(f"Totals as of: {formatted_time}\n")
        file.write(f"\n".join(lines))
        file.write("\n")
    # Saves the macronutrient total to the log file

def display_food_info(food):
    """
    Displays the macronutrient content of a a selected food 

        Parameters: 
        Food: A list containing the food name and the macronutrient content

        Return: None
    """
    print("-" * 40)
    print(food[FOOD_NAME_INDEX])
    print("-" * 40)
    print(f"{'Category:':<18}{food[CATEGORY_INDEX]}")
    print(f"{'Serving size:':<18}{food[SERVING_INDEX]} g")
    print(f"{'Calories:':<18}{food[CALORIE_INDEX]} kcal")
    print(f"{'Protein:':<18}{food[PROTEIN_INDEX]} g")
    print(f"{'Carbohydrates:':<18}{food[CARBOHYDRATE_INDEX]} g")
    print(f"{'Fat:':<18}{food[FAT_INDEX]} g")
    print(f"{'Saturated fat:':<18}{food[SAT_FAT_INDEX]} g")
    print("-" * 40)
    # A series of print statements 
    # to display the food macronutrient content

def find_foods(search, dictionary):
    """
    Allows user to search for foods within the dictionary 
    using a regex styled system

        Parameters: 
        search: The input from the user. This string will be compared to the 
                different food names in the list to find any matches
        dictionary: The food dataset, foods.csv
    
        Return: a list of possible matches
    """
    search = search.lower().strip()
    matches = {}
    # Turns user input into all lowercase and strips it of any whitespace
    # and creates the dictionary matches

    for foodname, row, in dictionary.items():
        if search in foodname.lower():
            matches[foodname] = row
            # Loops through the dictionary comparing the user search to
            # all of the food names in the dictionary. If a match is found
            # the food and macronutrients will be added to the dictionary matches
    return matches

def display_foods_by_category(dictionary):
    """
    Displays the dataset of food in a clean legible and organized way. 
    Each food is sorted and displayed by category

        Parameters:
        Dictionary: The dataset of foods 

        Return: none
    """
    categories = {}

    for food_name, row in dictionary.items():
        category = row[CATEGORY_INDEX]
        categories.setdefault(category, []).append(food_name)
        # Loops through the dictionary appending foods to their respective 
        # categories

    for category in sorted(categories):
        print("\n" + "=" * 40)
        print(f"{category:^40}")
        print("=" * 40)
        # Prints the category and an empty table

        for food_name in sorted(categories[category]):
            print(f"  {food_name}")
        # Prints each food in their respective category


def main():
    """
    The main function of the program. The user will have 6 options
    1: To browse each food in the food dataset
    2: Log a food to their daily total
    3: View the macronutrients of a specific food
    4: Add a new food to the food dataset
    5: Display and save daily totals to the log file
    6: Exit the program without saving daily totals
    
        Parameters: None

        Return: None
    """

    filename = "foods.csv"
    logfile =  "foodlog.txt"
    dictionary = read_dictionary(filename, FOOD_NAME_INDEX)
    portions = []
    run = True
    # Assigns filename, logfile, dictionary, portions, and run variables

    while run:
        print("\n" + "=" * 40)
        print("           MACRO CALCULATOR")
        print("=" * 40)
        print("1. Browse foods by category")
        print("2. Log a food")
        print("3. View food information")
        print("4. Add a new food to the food dataset")
        print("5. Finish and show daily totals")
        print("6. Exit without saving totals")
        print("=" * 40)
        # Prints the menu to the user

        usr_in = input("Enter your choice: ").strip()
        # Gathers user input, removing any whitespace

        if usr_in == "1":
            display_foods_by_category(dictionary)
            # Calls display foods by category, displaying the list of foods
            # in their respective category

            input("\nPress enter to continue: ")
            # Empty input function to delay menu from popping up  

        elif usr_in == "2":
            search = input("Enter a food: ")
            matches = find_foods(search, dictionary)
            # Searches food dataset for a match based on the user input

            if len(matches) == 0:
                print("No foods found")
            # If there are no matches print no foods found
            
            elif len(matches) == 1:
                food_name = list(matches.keys())[FOOD_NAME_INDEX]
                selected_food = matches[food_name]
                display_food_info(selected_food)
                # If there is one match, the food info will automatically be
                # assigned to the selected foods list. The display food info 
                # will then be called 
            
                try:
                    grams = float(input("How many grams did you eat? "))
                    # Gather user input for portion size

                except ValueError:
                    print("Error: Please enter a number for grams")
                    # Errors out if user does not enter a number

                else:
                    portion = portion_calc(selected_food, grams)
                    portions.append(portion)
                    print(f"{food_name.title()} added to your daily total")
                    # If there are no errors then the food macronutrients will
                    # be added to the list portions which will contribute to 
                    # daily totals

            else:
                print("\nMatching foods:")

                food_names = list(matches.keys())
                for i, food_name, in enumerate(food_names, start=1):
                    print(f"{i}. {food_name}")
                # If there are multiple foods that match the search then
                # the list of matching foods will print to the terminal.
                # The user will have the decision to select the correct food

                try: 
                    selection = int(input("Select a food: "))

                except ValueError:
                    print("Error: Invalid input. Please type a number")
                    # Errors out if a number is not entered
                else:
                    if selection < 1 or selection > len(food_names):
                        print("Error: Number out of range of options")
                        # Catches numbers out of range
                    else:
                        food_name = food_names[selection - 1]
                        selected_food = matches[food_name]
                            
                        display_food_info(selected_food)
                        # If there are no errors then the food info will be 
                        # assigned to the list selected foods

                        try:
                            grams = float(input("How many grams did you eat? "))
                        except ValueError:
                            print("Error: Please enter a number for grams")
                            # Errors out if a wrong value is entered
                        else:
                            portion = portion_calc(selected_food, grams)
                            portions.append(portion)
                            print(f"{food_name.title()} added to your daily total")
                            # If no errors occur then the portion of food will
                            # Be added to the portions list which will contribute
                            # to the daily total
        
        
        elif usr_in == "3":
            search = input("Enter a food: ")
            matches = find_foods(search, dictionary)
            # Compares the user input to the list of food names

            if len(matches) == 0:
                print("No food found")
            # If there are no matches print no food found

            elif len(matches) == 1:
                food_name = list(matches.keys())[FOOD_NAME_INDEX]
                selected_food = matches[food_name]
                display_food_info(selected_food)
            # If there is one food found then the food will automatically
            # display the food and macronutrient content to the terminal

            else:
                print("\nMatching foods:")

                food_names = list(matches.keys())
                # If more than one food is found then the a list of food names
                # will be displayed 

                for number, food_name in enumerate(food_names, start=1):
                    print(f"{number}. {food_name}")
                # List of food names displayed

                try:
                    selection = int(input("Choose a food number: "))
                    # User selects the food
                except ValueError:
                    print("Error: invalid input")
                    # Errors out if the value is not an int
                
                else:    
                    if selection < 1 or selection > len(food_names):
                        print("Error: Number out of range of options")
                    # Errors out if the input is out of range
                    else:
                        food_name = food_names[selection - 1]
                        selected_food = matches[food_name]  
                        display_food_info(selected_food)
                    # If no error occurs the food and its macronutrient content
                    # will be displayed to the terminal
        
        elif usr_in == "4":
            add_food(filename)
            # Calls the add food function

            dictionary = read_dictionary(filename, FOOD_NAME_INDEX)
            # Reloads the dictionary 

            input("Press enter to continue: ")
            # Empty input function to delay the menu from popping up

        elif usr_in == "5":
            totals = calc_totals(portions)
            # Assigns the macronutrient totals to the variable totals by 
            # calling the calc_totals function
            
            display_print_totals(totals, logfile)
            # Calls the display_print_totals function

            run = False
            # Assigns run to false ending the loop and the program
        
        elif usr_in == "6":
            print("Exiting without saving. Goodbye")
            run = False
            # Prints a goodbye message and assigns run to false
            # ending the loop and the program 

        else:
            print("Invalid input: Please try again")
            # Catches invalid inputs 
            input("Press enter to continue: ")
            # Empty input function to delay the menu from popping up

if __name__ == "__main__":
    main()
# Runs the program

