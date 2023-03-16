"""
Nom : Tulkens
Prénom : Alexandre
Matricule : 000575251
"""
from pos2d import Pos2D


class Box:
    def __init__(self, pos1: Pos2D, pos2: Pos2D):
        self.__top_left = pos1
        self.__bot_right = pos2
        self.__width = pos2.x - pos1.x + 1
        self.__height = pos2.y - pos1.y + 1

    @property
    def top_l(self):
        return self.__top_left

    @property
    def bot_r(self):
        return self.__bot_right

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height
