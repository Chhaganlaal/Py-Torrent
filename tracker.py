import base64
import bencodepy
import json
import os
import socket
import hashlib
import sys
from util import *
from urllib.parse import urlparse

def udp_send(socket, message, url):
    socket.sendto(message, (url.hostname, url.port))

def resp_type(response):
    action = int(response[:4].hex(), 16)

    return 'connect' if action==0 else ('announce' if action==1 else None)

def build_conn_req():
    # buffer = bytes.fromhex('00000417')+bytes.fromhex('27101980')
    # buffer = buffer + bytes.fromhex('00000000')
    # buffer = buffer + os.urandom(4)

    buffer = (0x41727101980).to_bytes(8, 'big')
    buffer = buffer + (0).to_bytes(4, 'big')
    buffer = buffer + os.urandom(4)

    return buffer

def parse_conn_resp(response):
    ret = {
        'action': int(response[:4].hex(), 16),
        'transaction_id': int(response[4:8].hex(), 16),
        'connection_id': response[8:]
    }

    return ret

def build_announce_req(connID, torrent, port=6881):

    # Connection ID
    buffer = connID
    # Action
    buffer = buffer + (1).to_bytes(4, 'big')
    # Transaction ID
    buffer = buffer + os.urandom(4)
    # Info Hash
    buffer = buffer + get_info_hash(torrent)
    # Peer ID
    buffer = buffer + gen_id()
    # Downloaded
    buffer = buffer + (0).to_bytes(8, 'big')
    # Left
    buffer = buffer + get_torrent_length(torrent)
    # Uploaded
    buffer = buffer + (0).to_bytes(8, 'big')
    # Event
    buffer = buffer + (0).to_bytes(4, 'big')
    # IP Address
    buffer = buffer + (0).to_bytes(4, 'big')
    # Key
    buffer = buffer + os.urandom(4)
    # Num Want
    buffer = buffer + (0).to_bytes(4, 'big')
    # Port
    buffer = buffer + (port).to_bytes(2, 'big')

    return buffer

def parse_announce_resp(response):
    def group(iterable, groupSize):
        groups = []
        for i in range(0, len(iterable), groupSize):
            groups.append(iterable[i: i+groupSize])
        return groups
    
    def get_address(address):
        return {
            'ip': socket.inet_ntoa(address[0:4]),
            'port': socket.inet_ntop(socket.AF_INET, address[4:])
        }

    ret = {
        'action': int(response[:4].hex(), 16),
        'transaction_id': int(response[4:8].hex(), 16),
        'interval': int(response[8:12].hex(), 16),
        'leechers': int(response[12:16].hex(), 16),
        'seeders': int(response[16:20].hex(), 16),
        'peers': list(map(get_address, group(response[20:], 6)))
    }

    return ret

def getPeers(torrent):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        url = urlparse(torrent[b'announce'].decode())
        udp_send(sock, build_conn_req(), url)

        print(torrent[b'info'][b'length'])
        # sys.exit(0)

        # while True:
        response = sock.recv(4096)

        if resp_type(response)=='connect':
            conn_resp = parse_conn_resp(response)
            announce_req = build_announce_req(conn_resp['connection_id'], torrent)
            udp_send(sock, announce_req, url)
        elif resp_type(response)=='announce':
            print('response:', response, len(response))
            announce_resp = parse_announce_resp(response)
            print(announce_resp)
            return announce_resp['peers']
