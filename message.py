import os
import socket
import sys
from util import get_info_hash, gen_id

def build_handshake(torrent):

    # pstrlen
    buffer = (19).to_bytes(1, 'big')
    # pstr
    buffer += 'BitTorrent protocol'.encode()
    # reserved
    buffer += (0).to_bytes(8, 'big')
    # info hash
    buffer += get_info_hash(torrent)
    # peer id
    buffer += gen_id()

    return buffer

def build_keep_alive():

    buffer = (0).to_bytes(4, 'big')

def build_choke():

    # length
    buffer = (1).to_bytes(4, 'big')
    # id
    buffer += (0).to_bytes(1, 'big')

    return buffer

def build_unchoke():

    # length
    buffer = (1).to_bytes(4, 'big')
    # id
    buffer += (1).to_bytes(1, 'big')

    return buffer

def build_interested():

    # length
    buffer = (1).to_bytes(4, 'big')
    # id
    buffer += (2).to_bytes(1, 'big')

    return buffer

def build_uninterested():

    # length
    buffer = (1).to_bytes(4, 'big')
    # id
    buffer += (3).to_bytes(1, 'big')

    return buffer

def build_have(payload):

    # length
    buffer = (5).to_bytes(4, 'big')
    # id
    buffer += (4).to_bytes(1, 'big')
    # piece index
    buffer += (payload).to_bytes(4, 'big')

    return buffer

def build_bitfield(bitfield):

    # length
    buffer = (len(bitfield)+1).to_bytes(4, 'big')
    # id
    buffer += (5).to_bytes(4, 'big')
    # bitfield
    buffer += bitfield

    return buffer

def build_request(payload):

    # length
    buffer = (13).to_bytes(4, 'big')
    # id
    buffer += (6).to_bytes(1, 'big')
    # piece index
    buffer += (payload['index']).to_bytes(4, 'big')
    # begin
    buffer += (payload['begin']).to_bytes(4, 'big')
    # piece length
    buffer += (payload['length']).to_bytes(4, 'big')

    return buffer

def build_piece(payload):

    # length
    buffer = (len(payload['block'])+9).to_bytes(4, 'big')
    # id
    buffer += (7).to_bytes(1, 'big')
    # piece index
    buffer += (payload['index']).to_bytes(4, 'big')
    # begin
    buffer += (payload['begin']).to_bytes(4, 'big')
    # block
    buffer += (payload['block'])

    return buffer

def build_cancel(payload):

    # length
    buffer = (13).to_bytes(4, 'big')
    # id
    buffer += (8).to_bytes(1, 'big')
    # piece index
    buffer += (payload['index']).to_bytes(4, 'big')
    # begin
    buffer += (payload['begin']).to_bytes(4, 'big')
    # piece length
    buffer += (payload['length']).to_bytes(4, 'big')

    return buffer

def build_port(payload):

    # length
    buffer = (3).to_bytes(4, 'big')
    # id
    buffer += (9).to_bytes(1, 'big')
    # piece index
    buffer += (payload).to_bytes(4, 'big')

    return buffer

def parse_message(message):

    msg_id = int(message[4:5].hex(), 16) if len(message)>4 else None
    payload = message[5:] if len(message)>5 else None

    if msg_id in {6, 7, 8}:
        rest = payload[8:]

        payload = {
            'index': int(payload[0:4].hex(), 16),
            'begin': int(payload[4:8].hex(), 16)
        }

        payload[('block' if id==7 else 'length')] = rest

    return {
        'size': int(message[0:4].hex(), 16),
        'id': msg_id,
        'payload': payload
    }
