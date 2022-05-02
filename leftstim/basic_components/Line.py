import random

import numpy as np

from leftstim.basic_components.Point import Point
from leftstim.basic_components.Vector import Vector

class Line:
    def __init__(self, start_point, end_point):
        """generate Line instance that represents a non-curved line in 2D space, defined by
        start/end points
        :param start_point: starting point of line
        :type start_point: Point
        :param end_point: end point of line
        :type end_point: Point"""
        self.start_point = start_point
        self.end_point = end_point

    def draw(self, window, line_object):
        """draws the line in a specified window using a specified line object
        :param window: PsychoPy window to draw in
        :type window: psychopy.visual.Window
        :param line_object: PsychoPy line instance to draw with
        :type line_object: psychopy.visual.Line
        :return: None"""
        line_object.start = (self.start_point.x, self.start_point.y)
        line_object.end = (self.end_point.x, self.end_point.y)
        line_object.draw()

    def get_random_point(self):
        """returns a Point instance that is placed somewhere on the line
        :return: Point"""
        if self.is_horizontal():
            rand_x_coord = random.uniform(self.start_point.x, self.end_point.x)
            return Point(rand_x_coord, self.start_point.y)
        if self.is_vertical():
            rand_y_coord = random.uniform(self.start_point.y, self.end_point.y)
            return Point(self.start_point.x, rand_y_coord)
        rand_x_coord = random.uniform(self.start_point.x, self.end_point.x)
        delta_x = rand_x_coord - self.start_point.x
        rand_y_coord = delta_x * self.get_slope() + self.start_point.y
        return Point(rand_x_coord, rand_y_coord)

    def get_slope(self):
        """returns a coefficient representing this line's slope, i. e. the k in y = kx+m.
        if the line is actually horizontal or vertical, raise an error
        :return: float
        """
        if self.is_vertical() or self.is_horizontal():
            raise AttributeError("This is a horizontal or vertical line. You can't get the "
                                 "slope of horizontal/vertical lines.")
        delta_x = self.end_point.x - self.start_point.x
        delta_y = self.end_point.y - self.start_point.y
        return delta_y / delta_x

    def get_point_at_xcoord(self, xcoord):
        """returns a Point instance that represents a point on the line at the specified x coordinate
        :param xcoord: x coordinate
        :type xcoord: float
        :return: Point"""
        delta_x = xcoord - self.start_point.x
        delta_y = delta_x * self.get_slope()
        return self.start_point + Point(delta_x, delta_y)

    def get_point_at_ycoord(self, ycoord):
        """returns a Point instance that represents a point on the line at the specified y coordinate
        :param ycoord: y coordinate
        :type ycoord: float
        :return: Point"""
        delta_y = ycoord - self.start_point.y
        delta_x = delta_y / self.get_slope()
        return self.start_point + Point(delta_x, delta_y)

    def is_horizontal(self):
        """returns True if line's start_point and end_point have the same x-coordinate,
        i. e. the line is horizontal
        :return: bool"""
        return self.start_point.y == self.end_point.y

    def is_vertical(self):
        """returns True if line's start_point and end_point have the same y-coordinate,
        i. e. the line is vertical
        :return: bool"""
        return self.start_point.x == self.end_point.x

    def get_orientation(self):
        """returns the line's orientation as a string"""
        if self.is_vertical():
            return "vertical"
        if self.is_horizontal():
            return "horizontal"
        return "diagonal"

    def shift(self, x_shift, y_shift):
        """shift the line's points' positions by specified x/y numbers of steps
        :param x_shift: number of units to shift x-coordinates by
        :type x_shift: float
        :param y_shift: number of units to shift y-coordinates by
        :type y_shift: float
        :return: None"""
        self.start_point.shift(x_shift, y_shift)
        self.end_point.shift(x_shift, y_shift)

    def get_length(self):
        diff_point = self.end_point - self.start_point
        return (diff_point.x ** 2 + diff_point.y ** 2) ** (1 / 2)

    def get_max_dist(self, other):
        """returns the maximum point distance between this line and passed other line's start/end points
        :param other: Line instance
        return: double"""
        min_start_dist = min((self.start_point.dist(other.start_point), self.start_point.dist(other.end_point)))
        min_end_dist = min((self.end_point.dist(other.start_point), self.end_point.dist(other.end_point)))
        max_dist = max((min_start_dist, min_end_dist))
        return max_dist

    def get_dir_vector(self):
        """returns a vector representing the line's direction"""
        diff_point = self.end_point - self.start_point
        return Vector(diff_point.x, diff_point.y)

    def get_intersection(self, other):
        """returns the point where this and the passed other line intersect
        :param other: Line
        :return: Point"""
        this_dir_vec = self.get_dir_vector()
        other_dir_vec = other.get_dir_vector()
        this_arr = this_dir_vec.to_numpy()
        other_arr = other_dir_vec.to_numpy()
        # if cross product of vectors is close to 0, they are essentially paralell
        if np.abs(np.cross(this_arr, other_arr)) < 0.0001:
            raise AttributeError("lines for which intersection was sought are parallel")
        diff_point = other.start_point - self.start_point
        right_eq = np.array([[diff_point.x], [diff_point.y]])
        left_eq = np.concatenate((this_arr, other_arr)).reshape((-1, 2), order='F')
        this_vec_scalar, _ = np.linalg.solve(left_eq, right_eq)
        this_vec_scalar = np.asscalar(this_vec_scalar)
        intersect_point = Point(this_vec_scalar * this_dir_vec.x, this_vec_scalar * this_dir_vec.y) + self.start_point
        return intersect_point

    def fling_to_line(self, other_line):
        """returns a Line instance that has its starting point somewhere on this
        line, its end point somewhere on the other_line, and a length of a minimum of
        50 units (throws an error if this is not attainable)
        :param other_line: line that generated Line instance's end point should be placed on
        :type other_line: Line
        :return: Line"""
        from leftstim.basic_components.AttachedLine import AttachedLine

        distant_enough = False
        counter = 100
        while not distant_enough:
            if counter <= 0:
                raise AttributeError("tried to fling to a line that is too close")
            start_point = self.get_random_point()
            end_point = other_line.get_random_point()
            if start_point.dist(end_point) > 50:
                distant_enough = True
            counter -= 1
        return AttachedLine(start_point=start_point, end_point=end_point,
                            start_line=self, end_line=other_line)
    
    def get_extended_version(self, frame):
        """returns a line that has the same slope and positioning as this line, but that has been
        attached and extended to the passed frame's sides
        :param frame: Frame
        :return: AttachedLine
        """
        from leftstim.basic_components.AttachedLine import AttachedLine

        frame_top_y = frame.top_line.start_point.y
        frame_right_x = frame.right_line.start_point.x
        frame_bottom_y = frame.bottom_line.start_point.y
        frame_left_x = frame.left_line.start_point.x
        if self.is_horizontal():
            end_point = Point(frame_right_x, self.end_point.y)
            end_line = (frame.right_line)
            start_point = Point(frame_left_x, self.start_point.y)
            start_line = (frame.left_line)
        elif self.is_vertical():
            end_point = Point(self.end_point.x, frame_top_y)
            end_line = (frame.top_line)
            start_point = Point(self.start_point.x, frame_bottom_y)
            start_line = (frame.bottom_line)
        else:
            if self.end_point.x > self.start_point.x:
                leftmost_point, rightmost_point = self.start_point, self.end_point
            else:
                leftmost_point, rightmost_point = self.end_point, self.start_point
            line_k = (rightmost_point.y - leftmost_point.y) / (rightmost_point.x - leftmost_point.x)
            if line_k < 0 and abs((frame_right_x-leftmost_point.x) * line_k) < abs(leftmost_point.y-frame_bottom_y):
                new_y = (frame_right_x-leftmost_point.x) * line_k + leftmost_point.y
                new_x = frame_right_x
                end_point = Point(new_x, new_y)
                end_line = frame.right_line
            elif line_k < 0:
                new_y = frame_bottom_y
                new_x = (frame_bottom_y - leftmost_point.y)/line_k + leftmost_point.x
                end_point = Point(new_x, new_y)
                end_line = frame.bottom_line
            elif abs((frame_right_x-leftmost_point.x) * line_k) < abs(frame_top_y - leftmost_point.y):
                new_y = (frame_right_x-leftmost_point.x) * line_k + leftmost_point.y
                new_x = frame_right_x
                end_point = Point(new_x, new_y)
                end_line = frame.right_line
            else:
                new_y = frame_top_y
                new_x = (frame_top_y - leftmost_point.y)/line_k + leftmost_point.x
                end_point = Point(new_x, new_y)
                end_line = frame.top_line
            if line_k < 0 and abs((frame_left_x-leftmost_point.x) * line_k) < abs(frame_top_y - leftmost_point.y):
                new_y = (frame_left_x-leftmost_point.x) * line_k + leftmost_point.y
                new_x = frame_left_x
                start_point = Point(new_x, new_y)
                start_line = frame.left_line
            elif line_k < 0:
                new_y = frame_top_y
                new_x = (frame_top_y - leftmost_point.y)/line_k + leftmost_point.x
                start_point = Point(new_x, new_y)
                start_line = frame.top_line
            elif abs((frame_left_x-leftmost_point.x) * line_k) < abs(leftmost_point.y - frame_bottom_y):
                new_y = (frame_left_x-leftmost_point.x) * line_k + leftmost_point.y
                new_x = frame_left_x
                start_point = Point(new_x, new_y)
                start_line = frame.left_line
            else:
                new_y = frame_bottom_y
                new_x = -(leftmost_point.y - frame_bottom_y)/line_k + leftmost_point.x
                start_point = Point(new_x, new_y)
                start_line = frame.bottom_line
        return AttachedLine(start_point=start_point, end_point=end_point,
                            start_line=start_line, end_line=end_line)