import socket
import message
import job_queue
from util import *

class Peer(object):
    
    def __init__(self, address, torrent, args):

        self.__host = address['ip']
        self.__port = address['port']
        self.__torrent = torrent
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.method = args.method

        try:
            self.__sock.connect((self.__host, self.__port))
            print("Connection with peer '%s' successful\n" %(self.__host))
            self.__sock.settimeout(5)
        except:
            print("Could not connect to:", self.__host)
            return

        self.__queue = job_queue.Queue(self.__torrent)

    def download(self, client):

        # print("Establishing handshake...\n")
        handshake = message.build_handshake(self.__torrent)
        self.__sock.sendall(handshake)
        data = self.__sock.recv(4096)
        
        if not self.is_handshake(data):
            # print("Handshake not Received!!!")
            self.__sock.close()
            return
        else:
            # print("Handshake Acknowledged\n")
            self.__sock.sendall(message.build_interested())

        saved = bytes(0)
        msg_len = 0
        while True:
            try:
                msg = self.__sock.recv(4096)
                msg_len = int(msg[0:4].hex(), 16) + 4
                saved = saved + msg

                while len(saved)>=4 and len(saved)>=(int(saved[0:4].hex(), 16)+4):
                    msg_len = int(saved[0:4].hex(), 16) + 4
                    self.msg_handler(saved[:msg_len], client)
                    saved = saved[msg_len:]
            except socket.error:
                client.dump_received()
                break
    
    '''
    Message Handlers
    '''

    def msg_handler(self, msg, client):

        msg = message.parse_message(msg)

        if msg['id']==0: self.choke_handler()
        elif msg['id']==1: self.unchoke_handler(client)
        elif msg['id']==4: self.have_handler(msg['payload'], client)
        elif msg['id']==5: self.bitfield_handler(msg['payload'], client)
        elif msg['id']==7: self.piece_handler(msg['payload'], client)

    def is_handshake(self, msg):

        return (len(msg)==int(msg[:1].hex(), 16)+49) and (msg[1:20].decode()=='BitTorrent protocol')

    def choke_handler(self):
        
        self.__sock.close()

    def unchoke_handler(self, client):
        
        self.__queue.choked = False
        self.request_piece(client)

    def have_handler(self, payload, client):
        
        piece_index = int(payload[0:4].hex(), 16)
        queue_len = self.__queue.length()
        self.__queue.push(piece_index)

        if queue_len==0:
            self.request_piece(client)

    def bitfield_handler(self, payload, client):
        
        queue_len = self.__queue.length()

        bits = bin(int(payload.hex(), 16))[2:]
        bits = '0'*(get_number_of_pieces(self.__torrent)-len(bits)) + bits
        for i, bit in enumerate(bits):
            if bit=='1':
                self.__queue.push(i)
        
        if queue_len==0:
            self.request_piece(client)

    def piece_handler(self, payload, client):

        client.print_progress()
        
        if self.method==1:
            client.piece_to_file(payload, self.__torrent)
        elif self.method==2:
            offset = payload['index']*self.__torrent[b'info'][b'piece length'] + payload['begin']
            client.stream.seek(offset)
            client.stream.write(payload['block'])

        client.add_received(payload)
        
        if client.is_done():
            self.__sock.close()
            print("Progress:", 100)
            print("\nDownload Complete!!!")
        else:
            self.request_piece(client)

    def request_piece(self, client):

        if self.__queue.choked: 
            return None

        while self.__queue.length()>0:
            piece_block = self.__queue.poll()

            if client.needed(piece_block):
                self.__sock.sendall(message.build_request(piece_block))
                client.add_requested(piece_block)
                break
