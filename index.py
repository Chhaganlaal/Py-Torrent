import base64
import bencodepy
import json
import socket
import sys
import tracker
from urllib.parse import urlparse
bc = bencodepy.Bencode(encoding=None)

with open('puppy.torrent', 'rb') as f:
    torrent = bencodepy.bread(f)
    # print(torrent[b'announce'].decode())
    # print(str(torrent[b'announce'], 'utf-8'))
    tracker.getPeers(torrent)