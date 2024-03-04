from pos2d import Pos2D
import argparse


class Player:
    def __init__(self, start_position: Pos2D, params: argparse.Namespace):
        """
        Create a new Player object with all the attributes that a player will need,
        it's coordinates and it's vision

        :param start_position: starting point of player in grid
        :param params: Use view_radius and torch_delay
        """
        self.__pos = start_position
        self.__torch_radius = params.view_radius
        self.__torch_delay = params.torch_delay
        self.count_movement = 0

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.__pos = value

    @property
    def torch_radius(self):
        return self.__torch_radius

    @torch_radius.setter
    def torch_radius(self, value):
        self.__torch_radius = value

    @property
    def torch_delay(self):
        return self.__torch_delay

    def moved(self):
        """
        counts movement, checks for torch radius
        :return: None
        """
        self.count_movement += 1
        if self.count_movement % self.torch_delay == 0:
            self.torch_radius -= 1

    def move_up(self):
        """
        move player up
        """
        self.pos.y -= 1
        self.moved()

    def move_down(self):
        """
        move player down
        """
        self.pos.y += 1
        self.moved()

    def move_left(self):
        """
        move player left
        :return:
        """
        self.pos.x -= 1
        self.moved()

    def move_right(self):
        """
        move player right
        :return:
        """
        self.pos.x += 1
        self.moved()
