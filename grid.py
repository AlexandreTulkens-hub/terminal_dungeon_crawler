"""
Nom : Tulkens
Prénom : Alexandre
Matricule : 000575251
"""

class Node:
    def __init__(self, up, down, left, right):
        self.__up = up
        self.__down = down
        self.__left = left
        self.__right = right

    @property
    def up(self):
        return self.__up

    @up.setter
    def up(self, value):
        self.__up = value

    @property
    def down(self):
        return self.__up

    @down.setter
    def down(self, value):
        self.__down = value

    @property
    def left(self):
        return self.__up

    @left.setter
    def left(self, value):
        self.__left = value

    @property
    def right(self):
        return self.__up

    @right.setter
    def right(self, value):
        self.__right = value


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[None for j in range(width - 1)]for i in range(height - 1)]
