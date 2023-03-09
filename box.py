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
        self.__top_right = Pos2D(pos2.x, pos1.y)
        self.__bot_left = Pos2D(pos1.x, pos2.y)

    @property
    def top_l(self):
        return self.__top_left

    @property
    def top_r(self):
        return self.__top_right

    @property
    def bot_l(self):
        return self.__bot_left

    @property
    def bot_r(self):
        return self.__bot_right
