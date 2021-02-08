import os
import pickle
from copy import deepcopy
from util import *

class Client(object):

    def __init__(self, torrent):

        try:
            self.stream = open("pieces.sav", 'r+b')
        except:
            self.stream = open("pieces.sav", 'w+b')

        def build_array():
            number_of_pieces = get_number_of_pieces(torrent)
            arr = [[False for j in range(blocks_per_piece(torrent, i))] for i in range(number_of_pieces)]
            return arr

        try:
            self.load_received()
        except:
            self.__received = build_array()
            self.__requested = build_array()

            # print(self.__received)

    def add_requested(self, piece_block):

        block_index = int(piece_block['begin'] // BLOCK_LENGTH)
        self.__requested[piece_block['index']][block_index] = True

    def add_received(self, piece_block):

        block_index = int(piece_block['begin'] // BLOCK_LENGTH)
        self.__received[piece_block['index']][block_index] = True

    def needed(self, piece_block):

        if all(all(piece) for piece in self.__requested):
            self.__requested = deepcopy(self.__received)

        block_index = int(piece_block['begin'] // BLOCK_LENGTH)
        return not (self.__requested[piece_block['index']][block_index])

    def is_done(self):

        return all(all(piece) for piece in self.__received)

    def print_progress(self):

        downloaded = 0
        total = 0

        for piece in self.__received:
            for block in piece:
                if block:
                    downloaded += 1
                total += 1

        progress = (downloaded*100)//total

        print("progress:", progress, end='\n\n')

    def dump_received(self):

        with open("received.sav", 'wb') as f:
            pickle.dump(self.__received, f)

    def load_received(self):

        with open("received.sav", 'rb') as f:
            self.__received = pickle.load(f)
            self.__requested = deepcopy(self.__received)

