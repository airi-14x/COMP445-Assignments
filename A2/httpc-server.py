import socket
import threading
import argparse
from time import gmtime, strftime

import os
import sys

current_dir = os.getcwd()
response_body = ""
status_line = "HTTP/1.0 "
status_codes = {200 : "200 OK \r\n",
                201 : "201 Created \r\n",
                        400: "400 Bad Request \r\n",
                        404: "404 Not Found\r\n"}
def run_server(host,port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host,port))
        listener.listen(1)
        print('Server is listening at ', port)
        while True:
            conn,addr = listener.accept()
            threading.Thread(target = handle_client,args=(conn,addr)).start()
    finally:
        listener.close()

def handle_client(conn,addr):
    global response_body
    global status_line
    global status_codes
    print(addr, " has connected.")
    try:
        data = conn.recv(1024)
        
        request_text = data.decode('utf-8')
        print(request_text) 
        
        # Parsing the Request #
        request_content = request_text.split("\r\n\r\n")
        header_contents = request_content[0].split()
        request_method = header_contents[0]
        request_path = header_contents[1]
        
        request_body = None
        #only set request_body if a body exists
        if len(request_content)>1: 
            request_body = request_content[1]
        
        # Check whether GET/POST #
        if request_method == "GET":
            if len(request_path) == 1:
                show_directory()
                #call GET/
            else:
                print("GET/foo")
                return_content(request_path)
                #call GET/foo
        elif request_method == "POST" and request_body != None:
            print("POST /bar")
            write_file(request_path, request_body)
        else:
            print("Bad Req")
            status_line += status_code[400]
            #bad request
        
        #  Call GET / POST Functions #
        
        #
        #   Parsing and function calls end
        # Yep. We need to be able to tell if it's a 404 or a 200 and stuff like that. Those require going through the functions we made
        
        # Response Message #
        
        #status_line += status_codes[200]   # Need to set the status code 'n' value #  
   
        general_headers = "Date: "
        current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " GMT\r\n"
        general_headers += current_time
        general_headers += "Connection: close\r\n"
        
        response_headers = "Server: httpfs \r\nAccept-Ranges: bytes \r\n"
        body_length = len(response_body) #placeholder until body is ready 
       
        entity_headers = "Content-Type: text \r\nContent-Length: " + str(body_length) + "\r\n\r\n"
        response = status_line + general_headers + response_headers + entity_headers + response_body
        #dummy_response = "fake status line\r\nfake header \r\n\r\n body: request ack"
        #conn.sendall(dummy_response.encode('utf-8'))
        conn.sendall(response.encode('utf-8'))
        response_body = ""
        status_line = "HTTP/1.0 "
        #how does this look?, tried to keep the http message format but it's nice to know if we can send stuff back
    finally:
        conn.close()

def show_directory():
    global response_body
    global status_line
    global status_codes
    rootdir = os.getcwd()
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
        #if(file.endswith(".txt")): #example of having the request header "Accept : .txt"
            response_body+=( os.path.join(subdir, file)) + "\n"
    status_line += status_codes[200]
def return_content(request_path):
    global response_body
    global status_line
    global status_codes
    global current_dir
    request_path = current_dir+request_path
    # for foo.txt 
    #request_path = "subFolderA/foo.txt"
    if(os.path.isfile(request_path)):
        current_file = open(request_path,"r")
        response_body = current_file.read()
        #print(response_body)
        current_file.close()
        status_line += status_codes[200]
    else:
        status_line += status_codes[404]
        
def write_file(request_path,request_data):
    global response_body
    global status_line
    global status_codes
    global current_dir
    path_split = request_path.split("/")
    test_dir = ""
    for x in range(len(path_split)-1):
        test_dir += path_split[x] + "/"

    test_dir = current_dir + test_dir
    if os.path.isdir(test_dir):        
        request_path = current_dir+request_path   
        current_file = open(request_path,"w")
        current_file.write(request_data)
        current_file.close()
        response_body += path_split[-1] + " created.\r\n"
        response_body += "Size : " + str(os.path.getsize(request_path))
        response_body += "\r\nContent: {\r\n"
        current_file = open(request_path,"r")
        response_body += current_file.read()
        current_file.close()
        response_body += "\r\n}\r\n"
        status_line += status_codes[201]
    else:
        status_line += status_codes[400]

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
parser.add_argument("-v", help="printing debugging message", action="store_true")
parser.add_argument("-d", help="directory path", type=str, default=current_dir)
args = parser.parse_args()
current_dir = args.d
run_server('', args.port)

