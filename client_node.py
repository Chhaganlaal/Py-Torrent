from copy import deepcopy
from util import *

class Client(object):

    def __init__(self, torrent):

        def build_array():
            number_of_pieces = get_number_of_pieces(torrent)
            arr = [[False for j in range(blocks_per_piece(torrent, i))] for i in range(number_of_pieces)]
            return arr

        self.__requested = build_array()
        self.__received = build_array()

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