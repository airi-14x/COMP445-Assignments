import os
import sys
'''
root_dir = os.listdir()
print()

def check_dir(path):
	if path is not None:
		current_dir = os.listdir(path)
	else:
		current_dir = os.listdir(os.getcwd())
	for filename in current_dir:
		if(os.path.isdir(filename)):
			print("[Folder]" + filename)
			check_dir(filename)
		else:
			print(filename)
	
'''
rootdir = os.getcwd()
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
    	if(str(file).endswith(".txt")): #example of having the request header "Accept : .txt"
    		print( os.path.join(subdir, file))