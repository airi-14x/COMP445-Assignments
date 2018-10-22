import os

def read_file(filepath):
	if(os.path.isfile(filepath)):
		current_file = open(filepath,"r")
		body = current_file.read()
		print(body)
		current_file.close()
	else:
		print("404 Not Found")
		
print("Testing \"subFolderA/foo.txt\"")
read_file("subFolderA/foo.txt")
print("\n\nTesting \"foo.txt\"")
read_file("foo.txt")