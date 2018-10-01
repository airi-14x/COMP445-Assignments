import socket
import argparse
import sys
from argparse import RawTextHelpFormatter

def run_httpclient(host, port):

	try:
        # print("Request line? ")

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		sock.connect((host,port))

			#line = sys.stdin.readline(1024)
			#request = ("GET /status/418 HTTP/1.0\r\nHost: httpbin.org\r\n\r\n")
			#request = ("POST /post HTTP/1.0\r\nHost: httpbin.org\r\nContent-Length:\r\nContent-Type:application/json\r\nsmol:duck\r\n\r\nhello=me\r\n\r\n")
			#get req with args
			#full_request  = ("GET /get?course=networking&assignment=1 HTTP/1.0\r\nHost: httpbin.org\r\n\r\n")
			#full_request = full_request.encode("utf-8")

		#		POST
		request_line = ("POST /post HTTP/1.0\r\n")
		header_lines=("Host:httpbin.org\r\nContent-Type:application/json\r\n")
		body =("body=shown")
		header_lines+=("Content-length:" + str(len(body)) + "\r\n\r\n")
#
		full_request = (request_line+header_lines+body).encode("utf-8")


			#request = request.encode("utf-8")

            #request = line.encode("utf-8")
			#sock.sendall(request)

		sock.sendall(full_request)
		response = sock.recv(1024,socket.MSG_WAITALL)
		response = response.decode("utf-8")
		sys.stdout.write(response)

	finally:
		sock.close()

general_help = '''httpc is a curl-like application but supports HTTP protocol only. 
Usage: 
    httpc command [arguments]
The commands are: 
    get executes a HTTP GET request and prints the response.
    post executes a HTTP POST request and prints the response.
    help prints this screen.
    
Use "httpc help [command]" for more information about a command.

'''
        
get_help = '''usage: httpc get [-v] [-h key:value] URL

Get executes a HTTP GET request for a given URL. 

-v Prints the detail of the response such as protocol, status, and headers.
-h key:value Associates headers to HTTP Request with the format 'key:value'.

'''
        
post_help = '''usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL

Post executes a HTTP POST request for a given URL with inline data or from file.
     
-v Prints the detail of the response such as protocol, status, and headers.
-h key:value Associates headers to HTTP Request with the format 'key:value'.
-d string Associates an inline data to the body HTTP POST request.
-f file Associates the content of a file to the body HTTP POST request.

Either [-d] or [-f] can be used but not both.

'''
parser = argparse.ArgumentParser(description = (general_help + get_help+ post_help),formatter_class=RawTextHelpFormatter)
parser.add_argument("--host", help="server host", default="localhost")
parser.add_argument("--port", help="server port", type=int, default=8007)

#parser.add_argument("get", help = get_help)
#parser.add_argument("post", help = post_help)
parser.add_argument("httpc", type = str)

args = parser.parse_args()
print(args.httpc)
run_httpclient(args.host, args.port)
