import os
import bencodepy
import hashlib
import socket
from urllib.parse import urlparse

torrent_id = None

def gen_id():

    global torrent_id
    if not torrent_id:
        torrent_id = '-DM2021-'
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
        map(lambda l: size+l[b'length'], torrent[b'info'][b'files'])
    else:
        size = torrent[b'info'][b'length']

    return (size).to_bytes(8, 'big')

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
        url = torrent[b'announce']

        if url.scheme=='udp':
            return url

    return None

# print(gen_id())