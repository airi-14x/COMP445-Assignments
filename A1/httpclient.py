import socket
import argparse
import sys

# GET Request #
# Create Socket
# Bind socket to port of target host
# Encode raw request/(User input): <string>.encode("utf-8") to be sent as bytes
# Send encoded raw request via sendall : socket.sendall("raw request")
# receive response sock.recv(size<bytes>, socket.MSG_WAITALL)
# decode response to string with <string>.decode(“utf-8”) for display
# Close Socket connection.

def run_httpclient(host, port):

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((host,port))
        # print("Request line? ")
		while True:
			#line = sys.stdin.readline(1024)
			request = ("GET /status/418 HTTP/1.0\r\nHost: httpbin.org\r\n\r\n")
			request = request.encode("utf-8")
            #request = line.encode("utf-8")
			sock.sendall(request)

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
