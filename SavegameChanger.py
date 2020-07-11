import os
import configparser
from shutil import copy


# moves the correct profile into the game folder
def move_files(variables):
    for variable in variables:
        print(variable)


# initializes the program.
def initialize_program():
    config = configparser.ConfigParser()
    success_init = False
    while not success_init:
        try:
            config.read_file(open("SavegameChanger.ini"))
            success_init = True
        except FileNotFoundError:
            setup_ini()
    variables = []
    for section in config.sections():
        profile_local = [section, config[section]["name"], config[section]["path"]]
        variables.append(profile_local)
    return variables


# creates the necessary ini file and allows you to configure your Profiles
def setup_ini():
    amount = input("How many profiles do you want? ")
    config = configparser.ConfigParser()
    for number in range(1, int(amount) + 1):
        name_local = input("What name should profile " + str(number) + " have? ")
        config["Profile " + str(number)] = {"Name": name_local, "Path": "\\The Witcher 3\\SavegameChanger" + name_local}
    with open("SavegameChanger.ini", "w") as configfile:
        config.write(configfile)


initialized = initialize_program()
print("What would you like to do? ")
i = 0
for profile, name, path in initialized:
    i += 1
    print(str(i) + " load {}, named {}".format(profile, name))
max_choice = i
success_choice = False
while not success_choice:
    try:
        choice = input("Choice: ")
        choice = int(choice)
        if choice <= max_choice:
            success_choice = True
            move_files(initialized[choice - 1])
    except ValueError:
        print("invalid Choice")
