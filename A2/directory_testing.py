import os
import sys
root_dir = os.listdir()
print()

def check_dir(path):
	if path is not None:
		current_dir = os.listdir(path)
	else:
		current_dir = os.listdir()
	for filename in current_dir:
		if(os.path.isdir(filename)):
			filename = "[Folder]" + filename
		print(filename)
	pass

check_dir(None)