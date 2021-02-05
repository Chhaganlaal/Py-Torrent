import os
import bencodepy
import hashlib

torrent_id = None

def gen_id():
    global torrent_id
    if not torrent_id:
        torrent_id = '-DM0001-'
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
    size = torrent[b'info'][b'length']

    return (size).to_bytes(8, 'big')

# print(gen_id())