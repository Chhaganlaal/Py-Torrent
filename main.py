import base64
import bencodepy
import os
import socket
import sys

from urllib.parse import urlparse

import tracker
import peer_node
import client_node

bc = bencodepy.Bencode(encoding=None)

with open("The_Night_We_Met.torrent", 'rb') as f:

    torrent = bencodepy.bread(f)
    # print(torrent)
    # exit()

    client = client_node.Client(torrent)
    peers = tracker.getPeers(torrent)

    peer = peer_node.Peer(peers[0], torrent)
    peer.download(client)

    if client.is_done():
        client.stream.close()
        os.remove("received.sav")
