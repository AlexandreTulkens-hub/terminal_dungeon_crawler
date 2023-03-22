"""
Nom : Tulkens
Prénom : Alexandre
Matricule : 000575251
"""
from pos2d import Pos2D
from random import randint


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

    def opening_coordinates(self):
        """
        creates the coordinates between which there will be the entrance/exit of the box

        :return opening: coordinates of box opening
        :rtype: tuple(Pos2D)
        """

        x = randint(self.top_l.x, self.bot_r.x)
        if x == self.top_l.x or x == self.bot_r.x:
            y = randint(self.top_l.y, self.bot_r.y)
            if x == self.top_l.x:
                opening = (Pos2D(self.top_l.x, y), Pos2D(self.top_l.x - 1, y))
            else:
                opening = (Pos2D(self.bot_r.x, y), Pos2D(self.bot_r.x + 1, y))
        else:
            random = randint(0, 1)
            if not random:
                opening = (Pos2D(x, self.top_l.y), Pos2D(x, self.top_l.y - 1))
            else:
                opening = (Pos2D(x, self.bot_r.y), Pos2D(x, self.bot_r.y + 1))

        return opening
