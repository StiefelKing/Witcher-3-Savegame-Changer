import os

files = os.listdir("gamesaves")
for file in files:
    if file.endswith(".sc"):
        print(int(file[0:len(file) - 3]))
print("no active Profile found")
exit(-1)