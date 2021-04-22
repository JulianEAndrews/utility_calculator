import sys
import json
from datetime import datetime


def menu():
    print("\nSelect from the following menu options:")
    select = input(
        "1. Utility Calculator (u)\n2. User Menu (m)\n3. Exit (e)\n: "
    ).casefold()
    if select == "u" or select == "1":
        utility_sum()
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
    exit_menu()


def utility_calc(total):
    json_data = load_json()

    num_roommates = 0
    num_cats = 0
    # TODO: build out calculator
    for thing in json_data["people"]:
        print(thing["name"])
        print(thing["type"])
        room_type = thing["type"]
        if room_type == "roommate":
            num_roommates += 1
        elif room_type == "cat":
            num_cats += 1
        elif room_type == "kiln":
            kiln_cost = input("Input kiln cost: $")
            total = total - kiln_cost
    print(num_roommates)
    total_per = round(total / num_roommates, 2)
    print(f"${total_per}")

    exit_menu()


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
            elif user_input == "n" or user_input == "3":
                menu()
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

    time(json_data)

    json_data["people"].append(new_dict)

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
            print(f"{person_input} updated to: {edit_name}")
            print(f"Type: {edit_type}")

    dump_json(json_data)

    exit_menu()


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


def make_flt(prompt):
    """get input and validate type"""
    while True:
        try:
            var = float(input(prompt))
            return var
        except ValueError:
            print("Please enter a valid number.")


# TODO
# In Progress: Refactoring user menu.

# Completed: Create function that adds new roommate/cat to main database

# Use a chain map for default settings when initializing new list info. Check json.update/json.append
# Total cost of utilities -> calculate kiln cost, subtract kiln cost -> calculate price per day for bill period ->
# Charge cats and subtract that from total -> divide total remaining cost by number of roommates -> charge roommates
# if water month then factor in 2 month cost with days of cats


if __name__ == "__main__":
    print(
        "\n\n---Welcome to the automated Utility Tally of Information system or 'UTI'---"
    )
    menu()
