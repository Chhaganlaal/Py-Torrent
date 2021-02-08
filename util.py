import os
import bencodepy
import hashlib
import socket
import math
from urllib.parse import urlparse

torrent_id = None
BLOCK_LENGTH = int(math.pow(2, 14))

def gen_id():

    global torrent_id
    if not torrent_id:
        torrent_id = '-AT0001-'
        torrent_id = torrent_id.encode() + os.urandom(20-len(torrent_id))
    return torrent_id

def get_info_hash(torrent):

    info = bencodepy.encode(torrent[b'info'])
    hexdigest = hashlib.sha1(info).hexdigest()
    # print(hexdigest)
    info_hash = bytes.fromhex(hexdigest)
    # print(info_hash)

    return info_hash

def get_torrent_length(torrent):

    if b'files' in torrent[b'info']:
        size = 0
        for file_ in torrent[b'info'][b'files']:
            size += file_[b'length']
    else:
        size = torrent[b'info'][b'length']

    return (size).to_bytes(8, 'big')

def get_number_of_pieces(torrent):

    return int(len(torrent[b'info'][b'pieces']) // 20)

def get_udp_tracker(torrent):

    if b'announce-list' in torrent:
        url_lists = torrent[b'announce-list']

        for li in url_lists:
            for item in li:
                url = urlparse(item.decode())

                if url.scheme=='udp':
                    try:
                        socket.gethostbyname(url.hostname)

                        return url
                    except socket.error:
                        pass

    else:
        url = urlparse(torrent[b'announce'].decode())

        if url.scheme=='udp':
            return url

    return None

def piece_len(torrent, piece_index):

    total_length = int(get_torrent_length(torrent).hex(), 16)
    piece_length = torrent[b'info'][b'piece length']

    last_piece_length = total_length % piece_length
    last_piece_index = math.floor(total_length/piece_length)

    # print(total_length, ':', get_torrent_length(torrent), end=' : ')
    # print(piece_index, ':', last_piece_index, end=' : ')
    return last_piece_length if last_piece_index==piece_index else piece_length

def blocks_per_piece(torrent, piece_index):

    piece_length = piece_len(torrent, piece_index)
    # print(piece_index, ':', piece_length)

    return math.ceil(piece_length/BLOCK_LENGTH)

def block_len(torrent, piece_index, block_index):

    piece_length = piece_len(torrent, piece_index)

    last_block_length = piece_length % BLOCK_LENGTH
    last_block_index = math.floor(piece_length/BLOCK_LENGTH)

    return last_block_length if last_block_index==block_index else BLOCK_LENGTH

def get_bits(hex_val):

    int_val = int(hex_val, 16)

    ret = ''
    while int_val>0:
        ret = str(int_val%2) + ret
        int_val = int(int_val//2)

    return ret

# print(gen_id())