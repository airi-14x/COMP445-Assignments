import socket
import argparse
import sys

def run_httpclient(host, port):

	try:
        # print("Request line? ")
		while True:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			sock.connect((host,port))

			#line = sys.stdin.readline(1024)
			# GET request of Teapot
			# No Argument
			request = ("GET /status/418 HTTP/1.0\r\nHost: httpbin.org\r\n\r\n")

			#get req with args
			#full_request  = ("GET /get?course=networking&assignment=1 HTTP/1.0\r\nHost: httpbin.org\r\n\r\n")
			#full_request = full_request.encode("utf-8")

			request = request.encode("utf-8")

            #request = line.encode("utf-8")

			sock.sendall(full_request)
			response = sock.recv(1024,socket.MSG_WAITALL)
			response = response.decode("utf-8")
			sys.stdout.write(response)

	finally:
		sock.close()

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="server host", default="localhost")
parser.add_argument("--port", help="server port", type=int, default=8007)
args = parser.parse_args()
run_httpclient(args.host, args.port)
