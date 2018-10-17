import socket
import threading
import argparse

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
        print(data.decode('utf-8'))
        #I think our response will be completely different from the request. It's just resent in the example since it's echoserver
        #yep~ for now, we can do this
        #We'll be decoding, modifying the message with a response and sending it back?
        #right, so for our request, we would have to get whatever the request and write the correct
        # response. 
        
        #That's fine haha
        dummy_response = "fake status line\r\nfake header \r\n\r\n body: request ack"
        conn.sendall(dummy_response.encode('utf-8'))
        #how does this look?, tried to keep the http message format but it's nice to know if we can send stuff back
    finally:
        conn.close()
    
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
run_server('', args.port)

