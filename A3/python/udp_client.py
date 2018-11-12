import argparse
import ipaddress
import socket
import random

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
        send_SYN(conn,router_addr,router_port)
        # Receiving SYN-ACK #
        conn.settimeout(timeout)
        print('Waiting for SYN-ACK')
        expected_type = -1
        expected_seq = -1
        while(expected_type!=packet.SYN_ACK or expected_seq != (seq_num + 1)):
            response,sender = conn.recvfrom(1024)
            recv_pkt = Packet.from_bytes(response)
            expected_type = recv_pkt.packet_type

        ## Need to check out the server version of UDP Client to send the ACK
        ## Need to fix the Send ACK with the expected_seq
        ## Test the handshake ==> Resending packet version and the default version
      
        # Sending ACK #
        packet_type = packet.ACK
        #seq_num = -1 # Need to get ACK number from Server
        
        p = Packet(packet_type=packet_type,
                   seq_num=seq_num,
                   peer_ip_addr=peer_ip,
                   peer_port=server_port,
                   payload=msg.encode("utf-8"))
        
            
        # Try to receive a response within timeout
        
        print('Waiting for a response')
        response, sender = conn.recvfrom(1024)
        p = Packet.from_bytes(response)
        print('Router: ', sender)
        print('Packet: ', p)
        print('Payload: ' + p.payload.decode("utf-8"))

    except socket.timeout:
        print('No response after {}s'.format(timeout))
    finally:
        conn.close()

def send_SYN(conn, router_addr, router_port):
    print('Initiating three-way handshake\nSending SYN')
    packet_type = packet.SYN
    seq_num = random.randint(1,50)
    p = Packet(packet_type=packet_type,
                   seq_num=seq_num,
                   peer_ip_addr=peer_ip,
                   peer_port=server_port,
                   payload=msg.encode("utf-8"))
    conn.sendto(p.to_bytes(), (router_addr, router_port))
# Usage:
# python echoclient.py --routerhost localhost --routerport 3000 --serverhost localhost --serverport 8007

parser = argparse.ArgumentParser()
parser.add_argument("--routerhost", help="router host", default="localhost")
parser.add_argument("--routerport", help="router port", type=int, default=3000)

parser.add_argument("--serverhost", help="server host", default="localhost")
parser.add_argument("--serverport", help="server port", type=int, default=8007)
args = parser.parse_args()

run_client(args.routerhost, args.routerport, args.serverhost, args.serverport)
