"""
Nom : Tulkens
Prénom : Alexandre
Matricule : 000575251
"""
from pos2d import Pos2D
from box import Box


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
        for row in range(box.height):
            for column in range(box.width):
                if row == 0:  # Sets upper box border
                    self.grid[box.top_l.y][box.top_l.x + column].up = False
                if row == (box.height - 1):  # Sets lower box border
                    self.grid[box.top_l.y + row][box.top_l.x + column].down = False
                if column == 0:  # Sets left box border
                    self.grid[box.top_l.y + row][box.top_l.x].left = False
                if column == (box.width - 1):  # Sets right box border
                    self.grid[box.top_l.y + row][box.top_l.x + column].right = False

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
