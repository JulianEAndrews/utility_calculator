import sys
import json
from datetime import datetime


def menu():
    print("\nSelect from the following menu options:")
    select = input(
        "1. Utility Calculator (u)\n2. New Person (n)\n3. Exit (e)\n: "
    ).casefold()
    if select == "u" or select == "1":
        utility_sum()
    elif select == "n" or select == "2":
        new_person()
    elif select == "e" or select == "3":
        sys.exit()


def utility_sum():
    while True:
        water = make_flt("Give me the water bill: $")
        gas = make_flt("Give me the gas bill: $")
        internet = make_flt("Give me the internet bill: $")
        electricity = make_flt("Give me the electrical bill: $")
        conf = input(
            f"{water} {gas} {internet} {electricity}, correct?  "
        ).casefold()
        if conf in ["y", "yes"]:
            break

    total = water + gas + internet + electricity
    print(f"Utility Total: ${total}")

    utility_calc(total)

    select = (
        input("Would you like to return to the main (m)enu or (e)xit the program? ")
        .casefold()
        .strip()
    )
    if select == "m":
        menu()
    elif select == "e":
        sys.exit()


def make_flt(prompt):
    """get input and validate type"""
    while True:
        try:
            var = float(input(prompt))
            return var
        except ValueError:
            print("Please enter a valid number.")


def utility_calc(total):
    with open("test.json", "r") as json_file:
        json_data = json.load(json_file)
    # iterate through json data to add up number of roommates, cats, etc.
    num_roommates = 0
    num_cats = 0
    # TODO this is broked
    for thing in json_data["people"]:
        print(thing["name"])
        print(thing["type"])
        room_type = thing["type"]
        if room_type == "human":
            num_roommates += 1
        elif room_type == "cat":
            num_cats += 1
        elif room_type == "kiln":
            kiln_cost = input("Input kiln cost: $")
            total = total - kiln_cost
    print(num_roommates)
    total_per = round(total / num_roommates, 2)
    print(f"${total_per}")


# write function to delete or update an existing roommate.

def new_person():
    user_input = (
        input("Would you like to add a new person or item? Choose (y) or (n): ")
        .casefold()
        .strip()
    )
    if user_input == "y":
        with open("test.json", "r") as json_file:
            json_data = json.load(json_file)

        new_name = input("Name: ").title()
        new_type = input("Type (human, cat, item): ")
        new_dict = {"name": new_name, "type": new_type}

        date = datetime.now()
        timestamp = str(round(datetime.timestamp(date)))

        json_data["dt"] = timestamp
        json_data["people"].append(new_dict)

        with open("test.json", "w") as json_file:
            json.dump(json_data, json_file, indent=4)
    elif user_input == "n":
        menu()
    elif user_input == "e":
        sys.exit()
    else:
        menu()

# Use a chain map for default settings when intializing new list info.

# Total cost of utilties -> calculate kiln cost, subtract kiln cost -> calculate price per day for bill period ->
# Charge cats and subtract that from total -> divide total remaining cost by number of roommates -> charge roommates

# Complete: Create function that adds new roommate/cat to main database
# if water month then factor in 2 month cost with days of cats

if __name__ == "__main__":
    print(
        "\n\n---Welcome to the automated Utility Tally of Information system or 'UTI'---"
    )
    menu()
