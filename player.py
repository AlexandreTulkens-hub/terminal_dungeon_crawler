from grid import Grid
from pos2d import Pos2D
import argparse


class Player:
    def __init__(self, start_position: Pos2D, params: argparse.Namespace):
        """
        Create a new Player object with all the attributes that a player will need,
        it's coordinates and it's vision

        :param start_position: starting point of player in grid
        :param params: gonna use the visibility of the player on the grid and
                       when the visibility will decrement
        """
        self.__pos = start_position
        self.torch_radius = params.view_radius
        self.__torch_delay = params.torch_delay
        self.count_movement = 0

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.__pos = value

    def get_torch_radius(self):
        return self.torch_radius

    def move(self, direction: chr):
        if direction == "z":
            self.pos.y -= 1
        elif direction == "q":
            self.pos.x -= 1
        elif direction == "s":
            self.pos.y += 1
        else:
            self.pos.x += 1

        self.count_movement += 1
        if self.count_movement % self.torch_delay == 0:
            self.torch_radius -= 1

        return Pos2D(self.pos.x, self.pos.y)
