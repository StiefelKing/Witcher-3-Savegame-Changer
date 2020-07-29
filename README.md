# The Witcher 3 Savegame Changer
This little program helps you to use as many savegame "profiles" in The Witcher 3 as you like.

# Setup
Put either the .py or the .exe in your Documents/The Witcher 3 folder. (there should be a folder called gamesaves)
When you run the program for the first time, it'll go into the setup.
First it asks you how many profiles you want to create, then you have to give a name to each profile and tell it which one is the currently active one. 
The program now creates 
a) a folder called Profiles, with subfolders for backups and each profile, 
b) a File of the type x.sc in each Folder, that identifies the profile and 
c) an .ini, that links the number with the path and the name.

# Usage
Run the program, it'll prompt you to choose out of all possible profiles.
When you enter a number, it creates a backup of any files of the active profile, then moves the files from gamesaves to that folder and copys the files from the new active profile into gamesaves. You can start the game then
