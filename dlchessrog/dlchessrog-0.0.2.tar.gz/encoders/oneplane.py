import numpy as np 
import chess 
import chess.svg
from base import Encoder


class OnePlaneEncoder(Encoder):
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 1

    def name(self):  # <1>
        return 'oneplane'

    def encode(self, board):  # <2>
        board_matrix = np.zeros(self.shape())
        counter = 0
        for r in range(self.board_height):
            for c in range(self.board_width):
                if counter < 64:
                    p = board.piece_at(counter)
                    p = str(p)
                    color = board.color_at(counter)
                    if color is True:
                        if p == 'P':
                            board_matrix[0,r,c] = 1
                        elif p == 'B':
                            board_matrix[0,r,c] = 2
                        elif p == 'N':
                            board_matrix[0,r,c] = 3
                        elif p == 'R':
                            board_matrix[0,r,c] = 4
                        elif p == 'Q':
                            board_matrix[0,r,c] = 5
                        elif p == 'K':
                            board_matrix[0,r,c] = 6
                    else:
                        if p == 'p':
                            board_matrix[0,r,c] = -1
                        elif p == 'b':
                            board_matrix[0,r,c] = -2
                        elif p == 'n':
                            board_matrix[0,r,c] = -3
                        elif p == 'r':
                            board_matrix[0,r,c] = -4
                        elif p == 'q':
                            board_matrix[0,r,c] = -5
                        elif p == 'k':
                            board_matrix[0,r,c] = -6
                    counter += 1
        return board_matrix

# <1> We can reference this encoder by the name "oneplane".
# <2> To encode, we fill a matrix with 1 if the point contains one of the current player's stones, -1 if the point contains the opponent's stones and 0 if the point is empty.
# end::oneplane_encoder[]

# tag::oneplane_encoder_2[]
    def encode_point(self, point):  # <1>
        return 64 * (chess.square(chess.square_file(point.from_square), chess.square_rank(point.from_square))) + (chess.square(chess.square_file(point.to_square), chess.square_rank(point.to_square)))

    def decode_point_index(self, index):  # <2>
        froms = index // 64
        to = index % 64
        return (froms, to)

    def num_points(self):
        return self.board_width * self.board_height

    def shape(self):
        return self.num_planes, self.board_height, self.board_width

# <1> Turn a board point into an integer index.
# <2> Turn an integer index into a board point.
# end::oneplane_encoder_2[]


# tag::oneplane_create[]
def create(board_size):
    return OnePlaneEncoder(board_size)
# end::oneplane_create[]