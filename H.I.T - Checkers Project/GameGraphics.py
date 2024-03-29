
from GameBoard import *

class Graphics:
    def __init__(self):
        self.caption = "H.I.T Python Project - Checkers Game"
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.window_size = 600
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        self.background = pygame.image.load('resources/board.png')
        self.square_size = self.window_size / 8
        self.piece_size = self.square_size / 2

        self.message = False

    def setup_window(self):
        """
        This initializes the window and sets the caption at the top.
        """
        pygame.init()
        pygame.display.set_caption(self.caption)

    def update_display(self, board, legal_moves, selected_piece):
        """
        This updates the current display.
        """
        self.screen.blit(self.background, (0, 0))

        self.highlight_squares(legal_moves, selected_piece)
        self.draw_board_pieces(board)

        if self.message:
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)

        pygame.display.update()
        self.clock.tick(self.fps)


    def draw_board_squares(self, board):
        """
        Takes a board object and draws all of its squares to the display
        """
        for x in xrange(8):
            for y in xrange(8):
                pygame.draw.rect(self.screen, board[x][y].color,
                                 (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )

    def draw_board_pieces(self, board):
        """
        Takes a board object and draws all of its pieces to the display
        """
        for x in xrange(8):
            for y in xrange(8):
                if board.matrix[x][y].occupant != None:
                    pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, self.pixel_coords((x, y)),
                                       self.piece_size)

                    if board.location((x, y)).occupant.king == True:
                        pygame.draw.circle(self.screen, GOLD, self.pixel_coords((x, y)), int(self.piece_size),
                                           self.piece_size / 2)

    def pixel_coords(self, board_coords):
        """
        Takes in a tuple of board coordinates (x,y)
        and returns the pixel coordinates of the center of the square at that location.
        """
        return (
        board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

    def board_coords(self, (pixel_x, pixel_y)):
        """
        Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return (pixel_x / self.square_size, pixel_y / self.square_size)

    def highlight_squares(self, squares, origin):
        """
        Squares is a list of board coordinates.
        highlight_squares highlights them.
        """
        for square in squares:
            pygame.draw.rect(self.screen, HIGH, (
            square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))

        if origin != None:
            pygame.draw.rect(self.screen, HIGH, (
            origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

    def draw_message(self, message):
        """
        Draws message to the screen.
        """
        self.message = True
        self.font_obj = pygame.font.Font('freesansbold.ttf', 88)
        self.text_surface_obj = self.font_obj.render(message, True, (0, 0, 0), (255, 255, 255))
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (self.window_size/2, self.window_size/2)
