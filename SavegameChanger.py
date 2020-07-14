import os
import configparser
from shutil import copy, move
import datetime


class profile:
    counter = 0

    def __init__(self, name, number, path):
        if name or number or path is None:
            print("")
            #todo constructor for object from files or .ini
            return
        else:
            # constructor for objects from prompt
            self.name = name
            self.number = number
            self.path = path
            counter +=1


# moves the correct profile into the game folder
def move_files(variables, variables_backup):
    backup_files(variables_backup)
    print("Loading {}, named".format(variables[0], variables[1]))
    source = variables[2]
    destination = "gamesaves"
    files = os.listdir(source)
    for f in files:
        copy(source + "/" + f, destination)


# makes a backup of both the previous files in the profile folder
def backup_files(variables):
    print("Backing up {}, named {}.".format(variables[0], variables[1]))
    source1 = variables[2]
    destination1 = "profiles/_Backup/{}_{}/".format(variables[1], datetime.datetime.now().timestamp())
    if not os.path.exists(destination1):
        os.makedirs(destination1)
    files = os.listdir(source1)
    for f in files:
        move(source1 + "/" + f, destination1)
    print("Backing up gamesaves folder")
    source2 = "gamesaves"
    destination2 = "profiles/{}/".format(variables[1])
    if not os.path.exists(destination2):
        os.makedirs(destination2)
    files = os.listdir(source2)
    for f in files:
        move(source2 + "/" + f, destination2)


# checks which profile is loaded right now
def check_active():
    files = os.listdir("gamesaves")
    active_profile = "0"
    for file in files:
        if file.endswith(".sc"):
            active_profile = file
    return int(active_profile[0])


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
    directories = {"profiles", "profiles/_backup"}
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
    config = configparser.ConfigParser()
    for number in range(1, int(amount) + 1):
        name_local = input("What name should profile " + str(number) + " have? ")
        config["Profile " + str(number)] = {"Name": name_local,
                                            "Path": "profiles/" + name_local}
        if not os.path.exists("profiles/" + name_local):
            os.makedirs("profiles/" + name_local)
            open("profiles/" + name_local + "/{}.sc".format(str(number)), "w+")
    with open("SavegameChanger.ini", "w") as configfile:
        config.write(configfile)
    current = input("Which profile is the currently active one? (number) ")
    open("gamesaves/{}.sc".format(current), "w+")


initialized = initialize_program()
print("What would you like to do? ")
print("To rerun the initial setup delete or move the .ini file.")
print("the currently active Profile is named {}".format(check_active()))
print("0 exit")
i = 0
for profile, name, path in initialized:
    i += 1
    print(str(i) + " load {}, named {}".format(profile, name))
max_choice = i
success_choice = False
while not success_choice:
    try:
        choice = input("Choice: (number): ")
        choice = int(choice)
        if int(choice) == 0:
            exit(0)
        elif max_choice >= choice > 0:
            success_choice = True
            move_files(initialized[choice - 1], initialized[check_active() - 1])
    except ValueError:
        print("invalid Choice")
