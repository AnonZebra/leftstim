from leftstim.basic_components.Vector import Vector

class Point:
    def __init__(self, x, y):
        """generate Point instance that represents a specific point in 2D space
        :param x: x-coordinate
        :type x: float
        :param y: y-coordinate
        :type y: float"""
        self.x = x
        self.y = y
        self.grown = False

    def __key(self):
        return self.x, self.y

    def __eq__(self, other_point):
        if isinstance(other_point, Point):
            return self.__key() == other_point.__key()
        return NotImplemented

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __add__(self, other_point):
        """returns a new Point instance, with an x-coordinate resulting from adding
        this and the other_point's x coordinate values together, and a corresponding
        y-coordinate
        :param other_point: point to do addition with
        :type other_point: Point"""
        new_x = self.x + other_point.x
        new_y = self.y + other_point.y
        return Point(new_x, new_y)

    def __sub__(self, other_point):
        """returns a new Point instance, with an x-coordinate resulting from subtracting
        the other_point's x coordinate value from this point's x coordinate, and a corresponding
        y coordinate
        :param other_point: point to do addition with
        :type other_point: Point"""
        new_x = self.x - other_point.x
        new_y = self.y - other_point.y
        return Point(new_x, new_y)

    def __truediv__(self, scalar):
        """divides the point's coordinates by the passed scalar's value
        :param scalar: double"""
        new_x = self.x/scalar
        new_y = self.y/scalar
        return Point(new_x, new_y)

    def shift(self, x_shift, y_shift):
        """shift the point's position by specified x/y numbers of steps
        :param x_shift: number of units to shift x-coordinate by
        :type x_shift: float
        :param y_shift: number of units to shift y-coordinate by
        :type y_shift: float
        :return: None"""
        self.x += x_shift
        self.y += y_shift

    def grow_line(self, frame, orientation):
        """grow a line with the specified orientation from the point that runs between
        two of the passed frame's sides and return it, if a line hasn't already
        been grown from this point (in that case return False)
        :param frame: frame that the line is to run between
        :type frame: Frame
        :param orientation: "horizontal", "vertical" or "diagonal"
        :type orientation: string
        :return: AttachedLine or bool"""
        from leftstim.basic_components.AttachedLine import AttachedLine
    
        from leftstim.basic_components.FigureLine import FigureLine

        if self.grown:
            return False
        if orientation == "horizontal":
            return AttachedLine(start_point=Point(frame.left_line.start_point.x, self.y),
                                end_point=Point(frame.right_line.start_point.x, self.y),
                                start_line=frame.left_line,
                                end_line=frame.right_line)
        if orientation == "vertical":
            return AttachedLine(start_point=Point(self.x, frame.top_line.start_point.y),
                                end_point=Point(self.x, frame.bottom_line.start_point.y),
                                start_line=frame.top_line,
                                end_line=frame.bottom_line)
        random_frame_point = frame.get_random_point()
        mid_point = Point((self.x + random_frame_point.x)/2, (self.y + random_frame_point.y)/2)
        interim_line = FigureLine(Point(self.x, self.y), mid_point)
        interim_line.extend(frame)
        start_point = interim_line.start_ext_point
        end_point = interim_line.end_ext_point
        for frame_line in frame.lines:
            if start_point.is_on_line(frame_line):
                start_line = frame_line
            if end_point.is_on_line(frame_line):
                end_line = frame_line
        grown_line = AttachedLine(start_point=start_point, end_point=end_point,
                                  start_line=start_line, end_line=end_line)
        self.grown = True
        return grown_line

    def is_on_line(self, line):
        """checks if this point is on the specified line (0.001 unit degree of accuracy),
        and if so returns True, otherwise returns False
        :param line: line to check if point is on
        :type line: Line
        :return: bool"""
        if line.is_horizontal():
            if abs(line.start_point.y - self.y) < 0.001:
                return True
            return False
        if line.is_vertical():
            if abs(line.start_point.x - self.x) < 0.001:
                return True
            return False
        slope = line.get_slope()
        delta_x = self.x - line.start_point.x
        yhat = line.start_point.y + delta_x * slope
        if abs(yhat - self.y) < 0.001:
            return True
        return False

    def dist(self, other_point):
        """returns the euclidean distance between this and the passed other point"""
        return ((self.x-other_point.x)**2 + (self.y-other_point.y)**2)**(1/2)

    def get_dist_vector(self, other_point):
        diff_point = other_point - self
        return Vector(diff_point.x, diff_point.y)

    def is_in_frame(self, frame):
        """returns True if this point is inside of the passed frame, otherwise returns False"""
        is_in_x = (self.x >= frame.left_line.start_point.x) and (self.x <= frame.right_line.start_point.x)
        is_in_y = (self.y >= frame.bottom_line.start_point.y) and (self.y <= frame.top_line.start_point.y)
        return is_in_x and is_in_y
