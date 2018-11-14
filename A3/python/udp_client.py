import argparse
import ipaddress
import socket
import random
import packet as PKT

from packet import Packet

def run_client(router_addr, router_port, server_addr, server_port):
    peer_ip = ipaddress.ip_address(socket.gethostbyname(server_addr))
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timeout = 5
    
    try:
        # Packet Type:
        # 0: Data || 1: ACK || 2: SYN || 3: SYN-ACK || 4: NAK #
        #msg = "Hello World"
        #p = Packet(packet_type=0,
        #            seq_num=1,
        #           peer_ip_addr=peer_ip,
        #           peer_port=server_port,
        #           payload=msg.encode("utf-8"))
        #conn.sendto(p.to_bytes(), (router_addr, router_port))
        #print('Send "{}" to router'.format(msg))
        
        # Sending SYN #
        send_SYN(conn,router_addr,router_port,peer_ip,server_port)
        
        # Receiving SYN-ACK #
        conn.settimeout(timeout)
        print('Waiting for SYN-ACK')
        expected_type = PKT.SYN_ACK
        rcv_pkt_type = -1
        while(rcv_pkt_type!=PKT.SYN_ACK):
            response,sender = conn.recvfrom(1024)
            recv_pkt = Packet.from_bytes(response)
            rcv_pkt_type = recv_pkt.packet_type
            print('Payload for expected SYN_ACK: ' + recv_pkt.payload.decode("utf-8"))
        
        send_ACK(conn,recv_pkt.peer_ip_addr,recv_pkt.peer_port,recv_pkt.seq_num,peer_ip,server_port)
        ## Test the handshake ==> Resending packet version and the default version
               
    except socket.timeout:
        print('No response after {}s'.format(timeout))
    finally:
        conn.close()

def send_SYN(conn, router_addr, router_port,peer_ip,server_port):
    print('Initiating three-way handshake\nSending SYN')
    packet_type = PKT.SYN
    seq_num = random.randint(1,50)
    msg = "Initiating three-way handshake\nSending SYN"
    p = Packet(packet_type=packet_type,
                   seq_num=seq_num,
                   peer_ip_addr=peer_ip,
                   peer_port=server_port,
                   payload=msg.encode("utf-8"))
    conn.sendto(p.to_bytes(), (router_addr, router_port))

def send_ACK(conn, router_addr, router_port, seq_number,peer_ip,server_port):
    new_packet_type = PKT.ACK  
    new_peer_ip_addr = peer_ip  
    new_peer_port = server_port
    new_seq_num = seq_number + 1 
    print(new_seq_num)
    print ("Sending ACK")
    msg = "Sending ACK"
    p = Packet(packet_type=new_packet_type,
                   seq_num=new_seq_num,
                   peer_ip_addr=new_peer_ip_addr,
                   peer_port=new_peer_port,
                   payload=msg.encode("utf-8")) 
    conn.sendto(p.to_bytes(),(str(router_addr), router_port))
# Usage:
# python echoclient.py --routerhost localhost --routerport 3000 --serverhost localhost --serverport 8007    
parser = argparse.ArgumentParser()
parser.add_argument("--routerhost", help="router host", default="localhost")
parser.add_argument("--routerport", help="router port", type=int, default=3000)

parser.add_argument("--serverhost", help="server host", default="localhost")
parser.add_argument("--serverport", help="server port", type=int, default=8007)
args = parser.parse_args()

run_client(args.routerhost, args.routerport, args.serverhost, args.serverport)

