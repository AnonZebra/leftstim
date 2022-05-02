import numpy as np

class Vector:
    def __init__(self, x, y):
        """generate Vector instance that represents a vector in 2D space
        :param x: x-component
        :type x: float
        :param y: y-component
        :type y: float"""
        self.x = x
        self.y = y

    def __key(self):
        return self.x, self.y

    def __eq__(self, other_vector):
        if isinstance(other_vector, Vector):
            return self.__key() == other_vector.__key()
        return NotImplemented

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __add__(self, other_vector):
        """returns a new Vector instance, with an x-coordinate resulting from adding
        this and the other_vector's x coordinate values together, and a corresponding
        y-coordinate
        :param other_vector: vector to do addition with
        :type other_vector: Vector"""
        new_x = self.x + other_vector.x
        new_y = self.y + other_vector.y
        return Vector(new_x, new_y)

    def __sub__(self, other_vector):
        """returns a new Vector instance, with an x-coordinate resulting from subtracting
        the other_vector's x coordinate value from this vector's x coordinate, and a corresponding
        y coordinate
        :param other_vector: vector to do addition with
        :type other_vector: Vector"""
        new_x = self.x - other_vector.x
        new_y = self.y - other_vector.y
        return Vector(new_x, new_y)

    def __truediv__(self, scalar):
        """divides the vector's coordinates by the passed scalar's value
        :param scalar: double"""
        new_x = self.x/scalar
        new_y = self.y/scalar
        return Vector(new_x, new_y)

    def __mul__(self, scalar):
        """multiplies the vector's coordinates by the passed scalar's value
        :param scalar: double"""
        new_x = self.x*scalar
        new_y = self.y*scalar
        return Vector(new_x, new_y)

    def __neg__(self):
        new_x = -self.x
        new_y = -self.y
        return Vector(new_x, new_y)

    def get_norm(self):
        return (self.x**2 + self.y**2)**(1/2)

    def get_normalized_vector(self):
        """returns a vector with the same direction as this one, but with length 1"""
        return self / self.get_norm()
    
    def to_numpy(self):
        return np.array([self.x, self.y])
