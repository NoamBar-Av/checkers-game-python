import pygame
from pygame.locals import *
from GameControl import *
from GameShapes import *
from GameGraphics import *

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
HIGH = (160, 190, 255)

NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

class Board:
    def __init__(self):
        self.matrix = self.new_board()

    def new_board(self):
        """
        Create a new board matrix.
        """

        # initialize squares and place them in matrix

        matrix = [[None] * 8 for i in xrange(8)]


        for x in xrange(8):
            for y in xrange(8):
                if (x % 2 != 0) and (y % 2 == 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 != 0) and (y % 2 != 0):
                    matrix[y][x] = Square(BLACK)
                elif (x % 2 == 0) and (y % 2 != 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 == 0) and (y % 2 == 0):
                    matrix[y][x] = Square(BLACK)

        # initialize the pieces and put them in the appropriate squares

        for x in xrange(8):
            for y in xrange(3):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(RED)
            for y in xrange(5, 8):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(GREY)

        return matrix

    def board_string(self, board):
        """
        Takes a board and returns a matrix of the board space colors. Used for testing new_board()
        """

        board_string = [[None] * 8] * 8

        for x in xrange(8):
            for y in xrange(8):
                if board[x][y].color == WHITE:
                    board_string[x][y] = "WHITE"
                else:
                    board_string[x][y] = "BLACK"

        return board_string

    def rel(self, dir, (x, y)):
        """
        Returns the coordinates one square in a different direction to (x,y).
        ===DOCTESTS===
        >>> board = Board()
        >>> board.rel(NORTHWEST, (1,2))
        (0,1)
        >>> board.rel(SOUTHEAST, (3,4))
        (4,5)
        >>> board.rel(NORTHEAST, (3,6))
        (4,5)
        >>> board.rel(SOUTHWEST, (2,5))
        (1,6)
        """
        if dir == NORTHWEST:
            return (x - 1, y - 1)
        elif dir == NORTHEAST:
            return (x + 1, y - 1)
        elif dir == SOUTHWEST:
            return (x - 1, y + 1)
        elif dir == SOUTHEAST:
            return (x + 1, y + 1)
        else:
            return 0

    def adjacent(self, (x, y)):
        """
        Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
        """

        return [self.rel(NORTHWEST, (x, y)), self.rel(NORTHEAST, (x, y)), self.rel(SOUTHWEST, (x, y)),
                self.rel(SOUTHEAST, (x, y))]

    def location(self, (x, y)):
        """
        Takes a set of coordinates as arguments and returns self.matrix[x][y]
        This can be faster than writing something like self.matrix[coords[0]][coords[1]]
        """

        return self.matrix[x][y]

    def blind_legal_moves(self, (x, y)):
        """
        Returns a list of blind legal move locations from a set of coordinates (x,y) on the board.
        If that location is empty, then blind_legal_moves() return an empty list.
        """

        if self.matrix[x][y].occupant != None:

            if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == GREY:
                blind_legal_moves = [self.rel(NORTHWEST, (x, y)), self.rel(NORTHEAST, (x, y))]

            elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == RED:
                blind_legal_moves = [self.rel(SOUTHWEST, (x, y)), self.rel(SOUTHEAST, (x, y))]

            else:
                blind_legal_moves = [self.rel(NORTHWEST, (x, y)), self.rel(NORTHEAST, (x, y)),
                                     self.rel(SOUTHWEST, (x, y)), self.rel(SOUTHEAST, (x, y))]

        else:
            blind_legal_moves = []

        return blind_legal_moves

    def legal_moves(self, (x, y), hop=False):
        """
        Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
        If that location is empty, then legal_moves() returns an empty list.
        """

        blind_legal_moves = self.blind_legal_moves((x, y))
        legal_moves = []

        if hop == False:
            for move in blind_legal_moves:
                if hop == False:
                    if self.on_board(move):
                        if self.location(move).occupant == None:
                            legal_moves.append(move)

                        elif self.location(move).occupant.color != self.location(
                                (x, y)).occupant.color and self.on_board(
                                (move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (
                                move[0] - x), move[1] + (
                                move[1] - y))).occupant == None:  # is this location filled by an enemy piece?
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

        else:  # hop == True
            for move in blind_legal_moves:
                if self.on_board(move) and self.location(move).occupant != None:
                    if self.location(move).occupant.color != self.location((x, y)).occupant.color and self.on_board(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (
                            move[0] - x), move[1] + (
                            move[1] - y))).occupant == None:  # is this location filled by an enemy piece?
                        legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

        return legal_moves

    def remove_piece(self, (x, y)):
        """
        Removes a piece from the board at position (x,y).
        """
        self.matrix[x][y].occupant = None

    def move_piece(self, (start_x, start_y), (end_x, end_y)):
        """
        Move a piece from (start_x, start_y) to (end_x, end_y).
        """

        self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
        self.remove_piece((start_x, start_y))

        self.king((end_x, end_y))

    def is_end_square(self, coords):
        if coords[1] == 0 or coords[1] == 7:
            return True
        else:
            return False

    def on_board(self, (x, y)):

        if x < 0 or y < 0 or x > 7 or y > 7:
            return False
        else:
            return True

    def king(self, (x, y)):

        if self.location((x, y)).occupant != None:
            if (self.location((x, y)).occupant.color == GREY and y == 0) or (
                    self.location((x, y)).occupant.color == RED and y == 7):
                self.location((x, y)).occupant.king = True
