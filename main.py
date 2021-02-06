import base64
import bencodepy
import socket
import sys
import tracker
import download
from urllib.parse import urlparse

bc = bencodepy.Bencode(encoding=None)

with open('Beast With It.torrent', 'rb') as f:

    torrent = bencodepy.bread(f)
    print(torrent)
    # print(torrent[b'info'][b'piece length'])
    peers = tracker.getPeers(torrent)

    # print(peers)

    # for peer in peers:
    download.download(peers[0], torrent)