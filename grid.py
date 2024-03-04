"""
Nom : Tulkens
Prénom : Alexandre
Matricule : 000575251
"""
from pos2d import Pos2D
from box import Box
from copy import deepcopy
from random import randint


class Node:
    def __init__(self, up: bool, down: bool, left: bool, right: bool):
        """
        Create a new Node object with booleans as border indicators.
        (True for no border, False for border)

        :param up: Upper border of node
        :param down: Lower border of node
        :param left: left border of node
        :param right: right border of node
        """
        self.__up = up
        self.__down = down
        self.__left = left
        self.__right = right
        self.been_there = False  # Used in DFS

    @property
    def up(self):
        """returns the value of up"""
        return self.__up

    @up.setter
    def up(self, value):
        """sets the value of up"""
        self.__up = value

    @property
    def down(self):
        """returns the value of down"""
        return self.__down

    @down.setter
    def down(self, value):
        """sets the value of down"""
        self.__down = value

    @property
    def left(self):
        """returns the value of left"""
        return self.__left

    @left.setter
    def left(self, value):
        """sets the value of left"""
        self.__left = value

    @property
    def right(self):
        """returns the value of right"""
        return self.__right

    @right.setter
    def right(self, value):
        """sets the value of right"""
        self.__right = value


class Grid:
    def __init__(self, width: int, height: int):
        """
        Create a new Grid object with the given width and height and sets the borders of the grid.

        :param width: The width of the grid
        :param height: The height of the grid.
        """
        self.__width = width
        self.__height = height
        self.grid = []  # Create the base of the grid
        #  filling the grid with borders
        for i in range(height):
            row = []
            if i == 0:  # Sets upper grid border
                upper = False
            else:
                upper = True
            if i == (height - 1):  # Sets lower grid border
                lower = False
            else:
                lower = True
            for j in range(width):
                if j == 0:  # Sets left grid border
                    left = False
                else:
                    left = True
                if j == (width - 1):  # Sets right grid border
                    right = False
                else:
                    right = True
                row.append(Node(upper, lower, left, right))
            self.grid.append(row)

    def __getitem__(self, index: tuple):
        """method that allows instances of the class to be accessed using square brackets"""
        row, column = index
        return self.grid[row][column]

    def __setitem__(self, index: tuple, value: any):
        """method that allows instances of the class to change a cell by using square brackets"""
        row, column = index
        self.grid[row][column] = value

    def __deepcopy__(self, memo):
        """method that allows the grid of instances of the class to be deep copied"""
        new_grid = Grid(self.width, self.height)  # Create a new instance of the Array class
        new_grid.grid = deepcopy(self.grid, memo)  # Deep copy the grid attribute
        return new_grid

    @property
    def width(self):
        """returns width of grid"""
        return self.__width

    @property
    def height(self):
        """returns height of grid"""
        return self.__height

    def get_neighbours(self, point: Pos2D):
        """
        gets neighbours of point in the grid (neighbours are the vertically and horizontally adjacent
        boxes)

        :param point: position of point in grid
        :return: the neighbouring elements of point
        :rtype: set(Pos2D)
        """
        #  Create the limits where the point has possible neighbours
        i = k = -1
        j = l = 2

        # determine the actual neighbours
        if point.y == 0:
            i = 0
        if point.y == self.height - 1:
            j = 1
        if point.x == 0:
            k = 0
        if point.x == self.width - 1:
            l = 1

        # put them in a set to win in complexity compared to a list (O(1) instead of O(n))
        neighbours = set()
        for change_row in range(i, j):
            if change_row == 0:
                for change_column in range(k, l):
                    if change_column != 0:
                        neighbours.add(Pos2D(point.x + change_column, point.y))
            else:
                neighbours.add(Pos2D(point.x, point.y + change_row))

        return neighbours

    def add_wall(self, pos1: Pos2D, pos2: Pos2D):
        """
        adds a wall between pos1 and pos2 if vertically and horizontally adjacent

        :param pos1: reference position
        :param pos2: position used to compare with neighbours of reference position
        :return:None
        """
        neighbours = self.get_neighbours(pos1)  # takes in the list of all the neighbours
        if pos2 in neighbours:
            if pos2.y < pos1.y:  # if pos2 is the upper neighbour
                self.grid[pos2.y][pos2.x].down = False
                self.grid[pos1.y][pos1.x].up = False
            elif pos2.y > pos1.y:  # if pos2 is the lower neighbour
                self.grid[pos2.y][pos2.x].up = False
                self.grid[pos1.y][pos1.x].down = False
            elif pos2.x < pos1.x:  # if pos2 is the left neighbour
                self.grid[pos2.y][pos2.x].right = False
                self.grid[pos1.y][pos1.x].left = False
            else:  # if pos2 is the right neighbour
                self.grid[pos2.y][pos2.x].left = False
                self.grid[pos1.y][pos1.x].right = False

    def remove_wall(self, pos1: Pos2D, pos2: Pos2D):
        """
        removes a wall between pos1 and pos2 if vertically and horizontally adjacent

        :param pos1: reference position
        :param pos2: position used to compare with neighbours of reference position
        :return:None
        """
        neighbours = self.get_neighbours(pos1)  # takes in the list of all the neighbours
        if pos2 in neighbours:
            if pos2.y < pos1.y:  # if pos2 is the upper neighbour
                self.grid[pos2.y][pos2.x].down = True
                self.grid[pos1.y][pos1.x].up = True
            elif pos2.y > pos1.y:  # if pos2 is the lower neighbour
                self.grid[pos2.y][pos2.x].up = True
                self.grid[pos1.y][pos1.x].down = True
            elif pos2.x < pos1.x:  # if pos2 is the left neighbour
                self.grid[pos2.y][pos2.x].right = True
                self.grid[pos1.y][pos1.x].left = True
            else:  # if pos2 is the right neighbour
                self.grid[pos2.y][pos2.x].left = True
                self.grid[pos1.y][pos1.x].right = True

    def isolate_box(self, box: Box):
        """
        sets the box borders

        :param box: box we want to draw in the grid
        :return: None
        """
        # Add left and right borders
        left_col = box.top_l.x
        right_col = box.bot_r.x
        for row in range(box.top_l.y, box.bot_r.y + 1):
            self.add_wall(Pos2D(left_col, row), Pos2D(left_col - 1, row))
            self.add_wall(Pos2D(right_col, row), Pos2D(right_col + 1, row))

        # Add top and bottom borders
        top_row = box.top_l.y
        bottom_row = box.bot_r.y
        for col in range(box.top_l.x, box.bot_r.x + 1):
            self.add_wall(Pos2D(col, top_row), Pos2D(col, top_row - 1))
            self.add_wall(Pos2D(col, bottom_row), Pos2D(col, bottom_row + 1))

    def accessible_neighbours(self, pos: Pos2D):
        """
        gets the accessible neighbours (neighbours that have no wall between them and pos)
        of pos in the grid

        :param pos: reference position
        :return: the accessible neighbouring elements of the point
        :rtype: List[Pos2D]
        """
        neighbours = []
        cell = self.grid[pos.y][pos.x]  # cell of which we want the accessible neighbours
        # !! when no wall Node object will contain True
        if cell.up:
            neighbours.append(Pos2D(pos.x, pos.y - 1))
        if cell.down:
            neighbours.append(Pos2D(pos.x, pos.y + 1))
        if cell.left:
            neighbours.append(Pos2D(pos.x - 1, pos.y))
        if cell.right:
            neighbours.append(Pos2D(pos.x + 1, pos.y))

        return neighbours

    """def visible_neighbours(self, visibility, pos):
        
        Calculate the potential visible neighbours of a position in a grid
        :param visibility: the radius in which things are visible
        :param pos: position in middle of this radius
        :return: the list of visible neighbours
        
        vision = visibility + 1 if visibility % 2 else visibility
        neighbours = []
        for y in range(int(pos.y - (vision / 2) - 1), int(pos.y + (vision / 2) + 1)):
            for x in range(int(pos.x - (vision / 2) - 1), int(pos.x + (vision / 2) + 1)):
                neighbours.append(Pos2D(x, y))

        return neighbours"""

    def spanning_tree(self):
        """
        Extracts a spanning tree out of the grid

        :return: new instance of Grid object
        :rtype: Grid
        """
        spanningTree = deepcopy(self)
        start_pos = Pos2D(0, 0)
        dfs(spanningTree, start_pos)
        return spanningTree


def dfs(grid: Grid, pos: Pos2D):
    """
    depth first search algorithm that will generate a maze

    :param grid: grid in which you generate the maze
    :param pos: pos of the grid we look at
    :return:None
    """

    current_cell = grid[pos.y, pos.x]
    current_cell.been_there = True
    accessible_neighbours = grid.accessible_neighbours(pos)
    # for each accessible neighbour continue the dfs
    for i in range(len(accessible_neighbours)):
        rand_neighbour = accessible_neighbours.pop(randint(0, (len(accessible_neighbours) - 1)))
        potential_cell = grid[rand_neighbour.y, rand_neighbour.x]

        if potential_cell.been_there:
            grid.add_wall(pos, rand_neighbour)
        else:
            dfs(grid, rand_neighbour)
            grid.remove_wall(pos, rand_neighbour)
