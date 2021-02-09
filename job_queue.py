from collections import deque
from util import *

class Queue(object):

    def __init__(self, torrent):

        self.__torrent = torrent
        self.__queue = deque()
        self.choked = True

    def push(self, piece_index):

        number_of_blocks = blocks_per_piece(self.__torrent, piece_index)

        for i in range(number_of_blocks):
            piece_block = {
                'index': piece_index,
                'begin': int(i*BLOCK_LENGTH),
                'length': block_len(self.__torrent, piece_index, i)
            }
            self.__queue.append(piece_block)

    def poll(self):

        return self.__queue.popleft()

    def peek(self):

        return self.__queue[0]

    def length(self):

        return len(self.__queue)