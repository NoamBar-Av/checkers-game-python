import pygame
from pygame.locals import *

class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king

class Square:
    def __init__(self, color, occupant=None):
        self.color = color  # BLACK or WHITE
        self.occupant = occupant  # occupant is a Square object
