import socket
import threading
import argparse
from time import gmtime, strftime

import os
import sys

current_dir = os.getcwd()
response_body = ""
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
    print(addr, " has connected.")
    try:
        data = conn.recv(1024)
        
        request_text = data.decode('utf-8')
        print(request_text) 
        
        # Parsing the Request #
        request_contents = request_text.split("\r\n\r\n")
        header_contents = request_contents[0].split()
        request_method = header_contents[0]
        request_path = header_contents[1]
        # Check whether GET/POST #
        
        
        if request_method == "GET":
            if len(request_path) == 1:
                show_directory()
                #call GET/
            else:
                print("GET/foo")
                #call GET/foo
        elif request_method == "POST":
            print("POST /bar")
            #call POST/bar
        else:
            print("Bad Req")
            #bad request
        
        #  Call GET / POST Functions #
        
        #
        #   Parsing and function calls end
        # Yep. We need to be able to tell if it's a 404 or a 200 and stuff like that. Those require going through the functions we made
        
        # Response Message #
        status_line = "HTTP/1.0 "
        status_codes = {200 : "200 OK \r\n",
                        400: "400 Bad Request \r\n",
                        404: "404 Not Found\r\n"}
        status_line += status_codes[200]   # Need to set the status code 'n' value #  
   
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
        #how does this look?, tried to keep the http message format but it's nice to know if we can send stuff back
    finally:
        conn.close()

def show_directory():
    global response_body
    rootdir = os.getcwd()
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
        #if(file.endswith(".txt")): #example of having the request header "Accept : .txt"
            response_body+=( os.path.join(subdir, file)) + "\n"
        
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
parser.add_argument("-v", help="printing debugging message", action="store_true")
parser.add_argument("-d", help="directory path", type=str, default=current_dir)
args = parser.parse_args()
current_dir = args.d
run_server('', args.port)

