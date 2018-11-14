import argparse
import socket
import random

import packet as PKT #getting naming problems

from packet import Packet

new_seq_num = 0
expected_type = PKT.SYN 
def run_server(port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        conn.bind(('', port))
        print('Echo server is listening at', port)
        while True:
            data, sender = conn.recvfrom(1024)
            handle_client(conn, data, sender)

    finally:
        conn.close()


def handle_client(conn, data, sender):
    global expected_type
    global new_seq_num
    try:
        p = Packet.from_bytes(data)
        print("Router: ", sender)
        print("Packet: ", p)
        print("Payload: ", p.payload.decode("utf-8"))
        if(expected_type == PKT.SYN): 
            new_seq_num = random.randint(1,50) # Can be any number. For last packet, need to
                               
            new_packet_type = PKT.SYN_ACK  
            new_peer_ip_addr = p.peer_ip_addr  
            new_peer_port = p.peer_port
             
            
            expected_type = PKT.ACK #We'll be waiting for ACK after the packet is sent.
            msg = "Sending SYN_ACK"
            
            new_packet = Packet(packet_type = new_packet_type,
                                seq_num = new_seq_num,
                                peer_ip_addr=new_peer_ip_addr,
                                peer_port=new_peer_port,
                                payload =msg.encode("utf-8"))
            conn.sendto(new_packet.to_bytes(), sender)
       
        elif(expected_type == PKT.ACK):
            print(new_seq_num)
            if(Packet.from_bytes(data).seq_num == new_seq_num + 1):
                print("Connection established")
                expected_type = PKT.SYN # RESET

    except Exception as e:
        print("Error: ", e)
        expected_type = PKT.SYN # RESET


# Usage python udp_server.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
run_server(args.port)

