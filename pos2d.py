"""
Nom : Tulkens
Prénom : Alexandre
Matricule : 000575251
"""


class Pos2D:
    def __init__(self, x: int, y: int):
        """
        Create a new Point object with the given x and y coordinates.

        :param x: The x-coordinate of the point.
        :type x: float
        :param y: The y-coordinate of the point.
        :type y: float
        """
        self.x = x
        self.y = y

    def x_getter(self):
        """returns the value of x"""
        return self.x

    def x_setter(self, other):
        """sets x to the value of other"""
        self.x = other

    def y_getter(self):
        """returns the value of y"""
        return self.y

    def y_setter(self, other):
        """sets x to the value of other"""
        self.y = other

    def __eq__(self, other):
        """
        Compare this Point object to another object for equality.

        :param other: The other object to compare to.
        :type other: Any
        :return: True if the other object is a Point with the same x and y coordinates, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Pos2D):  # Check if the other object is of type Pos2D
            return NotImplemented  # if it's not, the equality will not be Implemented
        return self.x == other.x and self.y == other.y