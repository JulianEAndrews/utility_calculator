import sys
import json
from datetime import datetime


# Menus
def menu():
    print("\nSelect from the following menu options:")
    select = input(
        "1. Utility Calculator (u)\n2. User Menu (m)\n3. Exit (e)\n: "
    ).casefold()
    if select == "u" or select == "1":
        get_utilities()
    elif select == "m" or select == "2":
        user_menu()
    elif select == "e" or select == "3":
        sys.exit()


def exit_menu():
    select = (
        input("Would you like to return to the main (m)enu or (e)xit the program? ")
        .casefold()
        .strip()
    )
    if select == "m":
        menu()
    elif select == "e":
        sys.exit()


# Utilities
def get_utilities():
    while True:
        month_1 = check_month("Enter water month 1: ")
        month_2 = check_month("Enter water month 2/last month: ")
        month_3 = check_month("Enter next month: ")
        electricity = make_flt("Electricity bill: $")
        gas = make_flt("Gas bill: $")
        internet = make_flt("Internet bill: $")
        water = make_flt("Water bill: $")
        conf = input(
            f"{month_1} {month_2} {month_3} {electricity} {gas} {internet} {water}, correct? "
        ).casefold()
        if conf in ["y", "yes"]:
            json_data = load_json()
            month_dict = {"month_1": month_1, "month_2": month_2, "month_3": month_3}
            util_dict = {"electricity": electricity, "gas": gas, "internet": internet, "water": water}
            json_data["utilities"] = util_dict
            json_data["months"] = month_dict
            time(json_data)
            dump_json(json_data)
            print(json_data["months"])
            print(json_data["utilities"])
            utility_calc()


"""
def utility_sum():
    total = water + gas + internet + electricity
    print(f"Utility Total: ${total}")

    utility_calc(total)
    exit_menu()
"""


def utility_calc():
    json_data = load_json()

    num_roommates = 0
    num_cats = 0
    # TODO: build out calculator
    for person in json_data["people"]:
        print(person["name"])
        print(person["type"])
        room_type = person["type"]
        if room_type == "Roommate":
            num_roommates += 1
            person["month_1_mod"] = 1
            person["month_2_mod"] = 1
            person["month_3_mod"] = 1
        elif room_type == "Cat":
            num_cats += 1
            cat_name = person["name"]
            person["month_1_mod"] = make_flt(f"Enter {cat_name}'s Month 1 Mod: ")
            person["month_2_mod"] = make_flt(f"Enter {cat_name}'s Month 2 Mod: ")
            person["month_3_mod"] = make_flt(f"Enter {cat_name}'s Month 3 Mod: ")
        elif room_type == "Kiln":
            continue
            # kiln_cost = input("Input kiln cost: $")
    print(num_roommates)
    print(num_cats)

    water()

    exit_menu()


# TODO; update roommate and cat modifiers first
def water():
    json_data = load_json()
    month_1 = input("Enter first water month: ").casefold()
    month_2 = input("Enter second water month: ").casefold()
    bill_days = month_to_days(month_1) + month_to_days(month_2)
    water_per_day = json_data["utilities"]["water"] / bill_days

    for person in json_data["people"]:
        if person["type"] == "Cat":
            days_here = make_flt("How many days were they here?: ")/bill_days
            print(days_here)
            cat_owes = water_per_day * days_here
            print(cat_owes)

    for person in json_data["people"]:
        if person["type"] == "Roommate":
            roommate_owes = water_per_day * bill_days


def month_to_days(month):
    if month == "january":
        days = 31
    elif month == "february":
        days = 28
    elif month == "march":
        days = 31
    elif month == "april":
        days = 30
    elif month == "may":
        days = 31
    elif month == "june":
        days = 30
    elif month == "july":
        days = 31
    elif month == "august":
        days = 31
    elif month == "september":
        days = 30
    elif month == "october":
        days = 31
    elif month == "november":
        days = 30
    elif month == "december":
        days = 31
    return days


def check_month(prompt):
    """get input and validate type"""
    while True:
        try:
            month = str(input(prompt))
            if month not in ["january", "february", "march", "april",
                           "may", "june", "july", "august",
                           "september", "october", "november", "december"]:
                pass
            return month
        except ValueError:
            print("Please enter a month.")


def make_flt(prompt):
    """get input and validate type"""
    while True:
        try:
            var = float(input(prompt))
            return var
        except ValueError:
            print("Please enter a valid number.")


# Users
def user_menu():
    user_input = (
        input("Would you like to:\n1. Add a new person/item (a),\n"
              "2. Edit a person/item (e),\n"
              "3. Delete a person/item (d)?\n: ")
        .casefold()
        .strip()
    )
    while True:
        try:
            if user_input == "a" or user_input == "1":
                new_person()
            elif user_input == "e" or user_input == "2":
                edit_person()
            elif user_input == "d" or user_input == "3":
                delete_person()
            elif user_input == "e":
                sys.exit()
            else:
                menu()
        except KeyboardInterrupt:
            print("Interrupted")


def new_person():
    json_data = load_json()

    new_name = input("Name: ").title()
    new_type = input("Type (roommate, cat, item): ")
    new_dict = {"name": new_name, "type": new_type}

    json_data["people"].append(new_dict)
    print(json_data["people"])

    time(json_data)

    dump_json(json_data)

    exit_menu()


def edit_person():
    json_data = load_json()

    for thing in json_data["people"]:
        print(thing["name"], thing["type"])
    person_input = input("Please select person: ").title()

    for person in json_data["people"]:
        if person["name"] == person_input:
            edit_name = input("Name: ").title()
            edit_type = input("Type (roommate, cat, item): ").title()
            person["name"] = edit_name
            person["type"] = edit_type
            print("Update successful!")
            print(f"{person_input} -> {edit_name}")
            print(f"Type: {edit_type}")

    time(json_data)

    dump_json(json_data)

    exit_menu()


def delete_person():
    json_data = load_json()

    for person in json_data["people"]:
        print(person["name"], person["type"])
    person_input = input("Please select person: ").title()

    new = [x for x in json_data["people"] if not (x["name"] == person_input)]
    json_data["people"] = new
    print("Delete successful!")
    print(new)

    time(json_data)

    dump_json(json_data)

    exit_menu()


# json functions
def load_json():
    with open("test.json", "r") as json_file:
        json_data = json.load(json_file)

    return json_data


def dump_json(json_data):
    with open("test.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)


def time(json_data):
    date = datetime.now()
    timestamp = str(round(datetime.timestamp(date)))

    json_data["dt"] = timestamp
    return json_data


# TODO
# In Progress: Refactoring user menu.

# Completed: Create function that adds new roommate/cat to main database

# Total cost of utilities -> calculate kiln cost, subtract kiln cost -> calculate price per day for bill period ->
# Charge cats and subtract that from total -> divide total remaining cost by number of roommates -> charge roommates
# if water month then factor in 2 month cost with days of cats


if __name__ == "__main__":
    print(
        "\n\n---Welcome to the automated Utility Tally of Information system or 'UTI'---"
    )
    menu()
