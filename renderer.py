"""
Nom : Tulkens
Prénom : Alexandre
Matricule : 000575251
"""
import argparse
from grid import Grid, Node
from pos2d import Pos2D
from player import Player

# Top left corner wall dictionary, each character is represented by one or more binary codes
TL_WALL = {(True, False, True, False): "─", (False, True, False, True): "│", (True, False, False, True): "┘",
           (False, True, True, False): "┌", (True, True, False, False): "└", (False, False, True, True): "┐",
           (True, True, False, True): " ", (False, False, True, False): "┬", (True, True, True, False): "─",
           (False, False, False, True): "┤", (True, False, False, False): "┴", (False, True, True, True): " ",
           (True, True, True, True): " ", (False, False, False, False): "┼", (True, False, True, True): " ",
           (False, True, False, False): "├"}


class GridRenderer:
    def __init__(self, grid: Grid):
        self.grid = grid

    def top_left_char(self, pos: Pos2D):
        """
        Create a list of booleans that describe the top left corner character of the cell at position pos in grid
        :param pos: x and y coordinates of the cell
        :return: the boolean list
        :rtype: List[bool]
        """
        tl_char = []
        cell = self.grid
        w = self.grid.width
        h = self.grid.height
        # we try and build the top left char, so False means char needs to cover this part(because wall)
        # and True means char needs to let this part open (because no wall)

        # down part of char
        if pos.x == w or pos.y == h:
            if pos.y == h:
                tl_char.append(True)
            else:
                tl_char.append(False)
        else:
            tl_char.append(cell[pos.y, pos.x].left)
        # left part
        if pos.x == 0:
            tl_char.append(True)
        else:
            if pos.y == h:
                tl_char.append(False)
            else:
                tl_char.append(cell[pos.y, pos.x - 1].up)
        # up part
        if pos.x == 0 or pos.y == 0:
            if pos.y == 0:
                tl_char.append(True)
            else:
                tl_char.append(False)
        else:
            tl_char.append(cell[pos.y - 1, pos.x - 1].right)
        # right part
        if pos.x == w:
            tl_char.append(True)
        else:
            if pos.y == 0:
                tl_char.append(False)
            else:
                tl_char.append(cell[pos.y - 1, pos.x].down)
        return tuple(tl_char)

    def show(self):
        """
        Print out the grid representing the maze on the terminal

        :return: None
        """
        nb_row = self.grid.height + 1
        nb_column = self.grid.width + 1
        # access every pos where we draw its upper wall and left wall (+1 to include the right side of right
        # grid border and bottom side of bottom grid border)
        for row in range(nb_row):
            grid_top_row = ""  # top wall of cells
            grid_left_row = ""  # left wall of cells
            for column in range(nb_column):
                tl_char_bool = self.top_left_char(Pos2D(column, row))
                if not tl_char_bool[0]:  # represents the left wall when False
                    grid_left_row += "│   "
                else:
                    grid_left_row += " " * 4  # 4 because one cell is 4 char long

                tmp = TL_WALL[tl_char_bool]
                if tl_char_bool[3]:
                    tmp += " " * 3
                else:
                    tmp += "─" * 3
                grid_top_row += tmp

            print(grid_top_row.rstrip())
            print(grid_left_row.rstrip())


class Renderer(GridRenderer):
    def __init__(self, grid: Grid, player: Player, bonus_list: list[Pos2D],
                 exiting_pos: Pos2D, params: argparse.Namespace):
        super().__init__(grid)
        self.player = player
        self.bonus_list = bonus_list
        self.exiting_pos = exiting_pos
        self.bonus_radius = params.bonus_radius

    def check_win_loss(self):
        """
        Checks if won or lost the game
        :rtype: bool
        """
        ress = False
        if self.player.pos == self.exiting_pos:
            print("\n"
                  "You find the exit!!! Now you can go on and tell stories about what you lived down there.\n"
                  "")
            ress = True
        elif self.player.torch_radius == 0:
            print("\n"
                  "The torch is out! :(\n"
                  "You are lost in the dungeon without light.\n"
                  "You end up dying of hunger...\n"
                  "")
            ress = True

        return ress

    def objects_collapse(self):
        """
        Checks if player collapses with a game object, if true, it applies the supposed effect on the game
        :return: None
        """
        if self.player.pos in self.bonus_list:
            self.player.torch_radius += self.bonus_radius
            self.bonus_list.remove(self.player.pos)

    def move_player(self, direction: chr):
        """
        moves player when no wall in direction
        :param direction: char representing movement of character
        :return: None
        """
        p_pos = Pos2D(self.player.pos.x, self.player.pos.y)

        if direction == 'w':
            if self.grid[p_pos.y, p_pos.x].up:
                self.player.move_up()
        elif direction == 's':
            if self.grid[p_pos.y, p_pos.x].down:
                self.player.move_down()
        elif direction == 'a':
            if self.grid[p_pos.y, p_pos.x].left:
                self.player.move_left()
        elif direction == 'd':
            if self.grid[p_pos.y, p_pos.x].right:
                self.player.move_right()

    def show(self):
        """
        Print out the grid representing the maze on the terminal
        added Player, bonuses, visibility, ghosts

        :return: None
        """
        nb_row = self.grid.height + 1
        nb_column = self.grid.width + 1
        for row in range(nb_row):
            grid_top_row = ""  # top wall of cells
            grid_left_row = ""  # left wall of cells
            for column in range(nb_column):
                cell = Pos2D(column, row)
                tl_char_bool = self.top_left_char(cell)
                if not tl_char_bool[0]:  # represents the left wall when False
                    if cell == self.player.pos:
                        grid_left_row += "│ x "
                    elif cell in self.bonus_list:
                        grid_left_row += "│ @ "
                    elif cell == self.exiting_pos:
                        grid_left_row += "│ # "
                    else:
                        grid_left_row += "│   "
                else:
                    if cell == self.player.pos:
                        grid_left_row += "  x "
                    elif cell in self.bonus_list:
                        grid_left_row += "  @ "
                    elif cell == self.exiting_pos:
                        grid_left_row += "  # "
                    else:
                        grid_left_row += " " * 4  # 4 because one cell is 4 char long

                tmp = TL_WALL[tl_char_bool]
                if tl_char_bool[3]:
                    tmp += " " * 3
                else:
                    tmp += "─" * 3
                grid_top_row += tmp

            print(grid_top_row.rstrip())
            print(grid_left_row.rstrip())