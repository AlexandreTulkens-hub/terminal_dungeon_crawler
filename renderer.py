"""
Nom : Tulkens
Prénom : Alexandre
Matricule : 000575251
"""
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

                tmp = TL_WALL[tl_char_bool]
                if tl_char_bool[3]:
                    tmp += " " * 3
                else:
                    tmp += "─" * 3
                grid_top_row += tmp

            print(grid_top_row.rstrip())
            print(grid_left_row.rstrip())

"""
class Renderer(GridRenderer):
    def __init__(self, grid: Grid, player: Player, torch_recharges: list[Pos2D], bonus_radius, exiting_pos: Pos2D):
        super().__init__(grid)
        self.grid = grid
        self.player = player
        self.torch_recharges = torch_recharges
        self.bonus_radius = bonus_radius
        self.exiting_pos = exiting_pos

    def movement(self, direction: chr):
        current_pos = Pos2D(self.player.pos.x, self.player.pos.y)

        if (direction == "z" and self.grid[current_pos.y - 1][current_pos.x].up) or \
                (direction == "q" and self.grid[current_pos.y][current_pos.x - 1].left) or \
                (direction == "s" and self.grid[current_pos.y + 1][current_pos.x].down) or \
                (direction == "d" and self.grid[current_pos.y][current_pos.x + 1].right):
            new_pos = self.player.move(direction)
            if new_pos in self.torch_recharges:
                self.toch_recharges.remove(new_pos)
                self.player.torch_radius += self.bonus_radius
        return False

    def top_left_char(self, index: int, visibles: list[Pos2D]):
        tl_char = []
        cell = self.grid
        circle_diameter = self.player.torch_radius + 1 if self.player.torch_radius % 2 else self.player.torch_radius
        pos = visibles[index]
        # we try and build the top left char, so False means char needs to cover this part(because wall)
        # and True means char needs to let this part open (because no wall)

        # down part of char
        if (index % circle_diameter == 0 and index != circle_diameter * 2) or \
                (index % circle_diameter == circle_diameter - 1 and index != circle_diameter * 3 - 1):
            tl_char.append(True)
        else:
            tl_char.append(cell[pos.y, pos.x].left)
        # left part
        if index % circle_diameter == 0 or index % circle_diameter == circle_diameter - 1 or \
                index < circle_diameter or index > circle_diameter ** 2 - (circle_diameter + 1):
            tl_char.append(True)
        else:
            tl_char.append(cell[pos.y, pos.x - 1].up)
        # up part
        if index % circle_diameter == 0 or index % circle_diameter == circle_diameter - 1 or \
                index < circle_diameter or index > circle_diameter ** 2 - (circle_diameter + 1):
            tl_char.append(True)
        else:
            tl_char.append(cell[pos.y - 1, pos.x - 1].right)
        # right part
        if (index < circle_diameter and index != circle_diameter/2 - 1) or \
                (index > circle_diameter ** 2 - (circle_diameter + 1) and
                 index != circle_diameter**2 - circle_diameter/2 - 1):
            tl_char.append(True)
        else:
            tl_char.append(cell[pos.y - 1, pos.x].down)
        return tuple(tl_char)

    def show(self):
        visibility = self.player.get_torch_radius()
        visibility_list = self.grid.visible_neighbours(visibility, self.player.pos)

        nb_row = self.grid.height + 1
        nb_column = self.grid.width + 1
        # access every pos where we draw its upper wall and left wall (+1 to include the right side of right
        # grid border and bottom side of bottom grid border)
        for row in range(nb_row):
            grid_top_row = ""  # top wall of cells
            grid_left_row = ""  # left wall of cells
            for column in range(nb_column):
                if Pos2D(column, row) in visibility_list:
                    tl_char_bool = self.top_left_char(visibility_list.index(Pos2D(column, row)), visibility_list)
                    if not tl_char_bool[0]:  # represents the left wall when False
                        grid_left_row += "│ "
                    else:
                        grid_left_row += " " * 2

                    # adding the objects in the maze
                    if Pos2D(column, row) == self.player.pos:
                        grid_left_row += "X "
                    elif Pos2D(column, row) == self.exiting_pos:
                        grid_left_row += "# "
                    elif Pos2D(column, row) in self.torch_recharges:
                        grid_left_row += "@ "
                    else:
                        grid_left_row += "  "

                    tmp = TL_WALL[tl_char_bool]
                    if tl_char_bool[3]:
                        tmp += " " * 3
                    else:
                        tmp += "─" * 3
                    grid_top_row += tmp
                else:
                    grid_top_row += " " * 4
                    grid_left_row += " " * 4

            print(grid_top_row.rstrip())
            print(grid_left_row.rstrip())
"""