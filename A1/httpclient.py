import socket
import argparse
import sys


def run_httpclient(host, port):

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((host,port))
        # print("Request line? ")
		while True:
			#line = sys.stdin.readline(1024)
			#request = ("GET /status/418 HTTP/1.0\r\nHost: httpbin.org\r\n\r\n")
			#request = ("POST /post HTTP/1.0\r\nHost: httpbin.org\r\nContent-Length:\r\nContent-Type:application/json\r\nsmol:duck\r\n\r\nhello=me\r\n\r\n")
			request_line = ("POST /post HTTP/1.0\r\n")
			header_lines=("Host:httpbin.org\r\nContent-Type:application/json\r\n")
			body =("body=shown")
			header_lines+=("Content-length:" + str(len(body)) + "\r\n\r\n")

			full_request = (request_line+header_lines+body).encode("utf-8")

			'''EXAMPLE POST REQUEST LINE
				    request = ("POST /post HTTP/1.0\r\nHost: httpbin.org\r\nsmol:duck\r\n\r\n")
					Header information can be sent.
					Issue: sending body information
			'''
			#request = request.encode("utf-8")
			full_request = (request_line+header_lines+body).encode("utf-8")
            #request = line.encode("utf-8")
			#sock.sendall(request)
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
