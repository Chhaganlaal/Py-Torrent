import base64
import bencodepy
import socket
import sys

from urllib.parse import urlparse

import tracker
import peer_node
import client_node

bc = bencodepy.Bencode(encoding=None)

with open("Beast With It.torrent", 'rb') as f:

    torrent = bencodepy.bread(f)
    # print(torrent)
    # print(len(torrent[b'info'][b'pieces']))
    peers = tracker.getPeers(torrent)

    client = client_node.Client(torrent)
    print(torrent)

    peer = peer_node.Peer(peers[0], torrent)
    peer.download(client)

    # for peer_ in peers:
    #     peer = peer_node.Peer(peer_, torrent)
    #     peer.download(client)