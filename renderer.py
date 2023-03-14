"""
Nom : Tulkens
Prénom : Alexandre
Matricule : 000575251
"""
from grid import Grid
from pos2d import Pos2D


class GridRenderer:
    # Top left corner wall dictionary
    TL_WALL = {(True, False, True, False): "─", (False, True, True, False): "┌", (False, False, True, True): "┐",
               (False, False, True, False): "┬", (True, True, False, False): "└", (False, True, False, True): "│",
               (False, True, False, False): "├", (True, False, False, True): "┘", (True, False, False, False): "┴",
               (False, False, False, True): "┤", (False, False, False, False): "┼", (True, True, True, True): " ",
               (False, True, True, True): " "}

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

        """Function that prints out the grid representing the maze on the terminal"""
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

                tmp = self.TL_WALL[tl_char_bool]
                if tl_char_bool[3]:
                    tmp += " " * 3
                else:
                    tmp += "─" * 3
                grid_top_row += tmp

            print(grid_top_row.rstrip())
            print(grid_left_row.rstrip())
