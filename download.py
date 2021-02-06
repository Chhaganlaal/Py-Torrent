import base64
import bencode
import os
import socket
import sys

import message

def is_handshake(message):

    return (len(message)==int(message[:1].hex(), 16)+49) and (message[1:20].decode()=='BitTorrent protocol')

def choke_handler():
    pass

def unchoke_handler():
    pass

def have_handler():
    pass

def bitfield_handler():
    pass

def piece_handler():
    pass

def download(peer, torrent):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        try:
            sock.connect((peer['ip'], peer['port']))
            print("Connection with peer '%s' successful\n" %(peer['ip']))
            print("Establishing handshake...\n")
            handshake = message.build_handshake(torrent)
            sock.sendall(handshake)
        except:
            print("Could not connect to:", peer['ip'])
            return

        while True:
            data = sock.recv(4096)

            if data:
                if is_handshake(data):
                    sock.sendall(message.build_interested())
                else:
                    print(data)
                    msg = message.parse_message(data)
                    print(msg)
                    print(msg['payload'])

                    exit()
