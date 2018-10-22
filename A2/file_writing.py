import os

def write_file(filepath, data):
	#if(os.path.isfile(filepath)):
		current_file = open(filepath,"w")
		#body = current_file.read()
		current_file.write(data)
		#print(body)
		current_file.close()
	#else:
	#	print("404 Not Found")
		
#print("Testing \"subFolderA/foo.txt\"")
write_file("subFolderA/bar2.txt", "Hello world.!2")
#print("\n\nTesting \"foo.txt\"")
#read_file("foo.txt")