import os, sys

# Open a file
#path = "/COMP445-Assignments/A2"
cwd = os.getcwd()
dirs = os.listdir( cwd )

# This would print all the files and directories
for file in dirs:
   print (file)