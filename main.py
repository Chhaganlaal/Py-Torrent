import argparse
import bencodepy
import os

import tracker
import peer_node
import client_node

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-tp", "--torrent-path", dest="torrent_path", required=True, help="Path to Torrent File", metavar='\b')
parser.add_argument("-sp", "--save-path", dest="save_path", default="./", help="Destination for Downloaded File", metavar='\b')
parser.add_argument("-w", "--write-method", dest="method", default=1, type=int, help="1 -- Write File as Pieces Arrive\n2 -- Write File After all the Pieces Arrive", metavar='\b')

args = parser.parse_args()

bc = bencodepy.Bencode(encoding=None)

with open(args.torrent_path, 'rb') as f:

    torrent = bencodepy.bread(f)

    client = client_node.Client(torrent, args)
    peer_list = tracker.getPeers(torrent)

    print("Peer List:\n", peer_list)

    peer = peer_node.Peer(peer_list[3], torrent, args)
    peer.download(client)

    if client.is_done():
        if args.method==2:
            client.write_to_file()
            client.stream.close()
        if os.path.exists("received.sav"):
            os.remove("received.sav")
        if os.path.exists("pieces.sav"):
            os.remove("pieces.sav")
