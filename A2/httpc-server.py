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

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
run_server('', args.port)
