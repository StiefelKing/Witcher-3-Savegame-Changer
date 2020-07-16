import os
import configparser
from shutil import copy, move
import datetime


class Profile:

    def __init__(self, name_const, number_const, path_const):
        self.name = name_const
        self.number = number_const
        if path_const is None:
            # for objects from prompt
            self.path = "profiles/" + name_const
        else:
            # for objects from .ini
            self.path = path_const

    def export_config(self):
        config = configparser.ConfigParser()
        config[str(self.number)] = {"Name": self.name, "Path": self.path}
        with open("SavegameChanger.ini", "a") as configfile:
            config.write(configfile)

    def compare_number(self, number):
        if self.number == number:
            return True
        else:
            return False


# moves the correct profile into the game folder
def change_savegame(profile_local):
    print("Loading Profile {}, named {}".format(profile_local.number, profile_local.name))
    source = profile_local.path
    destination = "gamesaves"
    files = os.listdir(source)
    for f in files:
        copy(source + "/" + f, destination)


# makes a backup of both the previous files in the profile folder
def backup_savegames(profile_local):
    print("Backing up Profile {}, named {}.".format(profile_local.number, profile_local.name))
    source1 = profile_local.path
    destination1 = "profiles/_Backup/{}_{}/".format(profile_local.name, datetime.datetime.now().timestamp())
    if not os.path.exists(destination1):
        os.makedirs(destination1)
    files = os.listdir(source1)
    for f in files:
        move(source1 + "/" + f, destination1)
    print("Backing up gamesaves folder")
    source2 = "gamesaves"
    destination2 = "profiles/{}/".format(profile_local.name)
    if not os.path.exists(destination2):
        os.makedirs(destination2)
    files = os.listdir(source2)
    for f in files:
        move(source2 + "/" + f, destination2)


def get_profile(profiles_local, number):
    for profile_local in profiles_local:
        if int(profile_local.number) == number:
            return profile_local


def choose(profiles_local, max_choice_local):
    success_choice = False
    while not success_choice:
        try:
            choice = int(input("Choice: (number): "))
            if int(choice) == 0:
                exit(0)
            elif max_choice_local >= choice > 0:
                success_choice = True
                backup_savegames(get_profile(profiles_local, check_active()))
                change_savegame(get_profile(profiles_local, choice))
        except ValueError:
            print("invalid Choice")


# checks which profile is loaded right now
def check_active():
    files = os.listdir("gamesaves")
    for file in files:
        if file.endswith(".sc"):
            return int(file[0:len(file) - 3])
    print("no active Profile found")
    exit(-1)


# prints out the information on the profiles, numbers and choices
def prompt(profiles_local):
    print("What would you like to do? ")
    print("To rerun the initial setup delete or move the .ini file.")
    print("the currently active Profile is named {}".format(check_active()))
    print("0 exit")
    i = 0
    for profile in profiles_local:
        i += 1
        print(str(i) + " load profile {}, named {}".format(profile.number, profile.name))
    return i


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
    profiles_local = []
    for section in config.sections():
        profiles_local.append(Profile(config[section]["name"], section, config[section]["path"]))
    return profiles_local


# creates the necessary ini file and allows you to configure your Profiles
def setup_ini():
    amount = input("How many profiles do you want? ")
    directories = ["profiles", "profiles/_backup"]
    files = []
    for number in range(1, int(amount) + 1):
        name_local = input("What name should profile " + str(number) + " have? ")
        profile_local = Profile(name_local, number, None)
        profile_local.export_config()
        directories.append(profile_local.path)
        files.append([profile_local.number, profile_local.path])
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
    if not os.path.exists("gamesaves"):
        os.makedirs("gamesaves")
    current = input("Which profile is the currently active one? (number) ")
    files.append([current, "gamesaves"])
    for file in files:
        open(file[1] + "/{}.sc".format(file[0]), "w+")


profiles = initialize_program()
max_choice = prompt(profiles)
choose(profiles, max_choice)
