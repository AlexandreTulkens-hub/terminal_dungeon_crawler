"""
Nom : Tulkens
Prénom : Alexandre
Matricule : 000575251
"""


class Pos2D:
    def __init__(self, x: int, y: int):
        """
        Create a new Pos2D object with the given x and y coordinates.

        :param x: The x-coordinate of the position.
        :param y: The y-coordinate of the position.
        """
        self.__x = x
        self.__y = y

    @property
    def x(self):
        """returns the value of x"""
        return self.__x

    @property
    def y(self):
        """returns the value of y"""
        return self.__y

    def __hash__(self):
        """
        hashes the data stocked in this class

        :return: hashed data
        :rtype: int
        """
        return hash((self.__x, self.__y))

    def __eq__(self, other):
        """
        Compare this Pos2D object to another object for equality.

        :param other: The other object to compare to.
        :type other: Any
        :return: True if the other object is a Pos2D with the same x and y coordinates, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Pos2D):  # Check if the other object is of type Pos2D
            return NotImplemented  # if it's not, the equality will not be executed
        return self.x == other.x and self.y == other.y
