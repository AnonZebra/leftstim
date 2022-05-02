import random

from leftstim.basic_components.FigureLine import FigureLine

class Figure:
    locked_x = False
    locked_y = False
    all_points = []
    figure_name = "unnamed"

    def __init__(self, lines, frame):
        """ generate a Figure instance, defined by the passed list of lines
        :param lines: lines of which the figure consists
        :type lines: list of Line instances
        :param frame: frame that the figure is to be inside of
        :type frame: Frame
        """
        self.lines = [FigureLine(line.start_point, line.end_point) for line in lines]

        points_with_duplicates = [point for line in lines for point in [line.start_point, line.end_point]]
        self.unique_points = set(points_with_duplicates)
        for point in points_with_duplicates:
            if not sum([point is x for x in self.all_points]):
                self.all_points.append(point)

        self.closed = lines[0].start_point == lines[len(lines) - 1].end_point
        self.height = self.get_highest_y_coord() - self.get_lowest_y_coord()
        self.width = self.get_highest_x_coord() - self.get_lowest_x_coord()
        self.frame = frame

    def draw(self, window, line_object):
        """draws the figure in a specified window using a specified line object
        :param window: PsychoPy window to draw in
        :type window: psychopy.visual.Window
        :param line_object: PsychoPy line instance to draw with
        :type line_object: psychopy.visual.Line
        :return: None"""
        for line in self.lines:
            line.draw(window, line_object)

    def get_random_point(self):
        """ return a random point on one of the figure's lines (this process isn't entirely random -
        points on a short line have a higher likelihood of being returned)

        :return: Point
        """
        rand_line = random.choice(self.lines)
        return rand_line.get_random_point()

    def shift(self, x_shift, y_shift):
        """ shift all the figure's lines by the specified x/y shifts
        :param x_shift: number of units to shift x-coordinates by
        :type x_shift: float
        :param y_shift: number of units to shift y-coordinates by
        :type y_shift: float
        :return: None
        """
        for point in self.all_points:
            point.shift(x_shift, y_shift)

    def get_lowest_x_coord(self):
        return min([point.x for point in self.unique_points])

    def get_highest_x_coord(self):
        return max([point.x for point in self.unique_points])

    def get_lowest_y_coord(self):
        return min([point.y for point in self.unique_points])

    def get_highest_y_coord(self):
        return max([point.y for point in self.unique_points])

    def has_top_line(self):
        """ checks to see if there is a horizontal line at the top of the figure,
        and if so, returns True (otherwise returns False)
        :return: bool
        """
        horizontal_lines = [line for line in self.lines if line.is_horizontal()]
        top_lines = [line for line in horizontal_lines if line.start_point.y == self.get_highest_y_coord()]
        if top_lines:
            return top_lines
        return False

    def has_rightmost_line(self):
        """ checks to see if there is a vertical line at the rightmost edge of the figure,
        and if so, returns True (otherwise returns False)
        :return: bool
        """
        vertical_lines = [line for line in self.lines if line.is_vertical()]
        rightmost_lines = [line for line in vertical_lines if line.start_point.x == self.get_highest_x_coord()]
        if rightmost_lines:
            return rightmost_lines
        return False

    def has_bottom_line(self):
        """ checks to see if there is a horizontal line at the bottom of the figure,
        and if so, returns True (otherwise returns False)
        :return: bool
        """
        horizontal_lines = [line for line in self.lines if line.is_horizontal()]
        bottom_lines = [line for line in horizontal_lines if line.start_point.y == self.get_lowest_y_coord()]
        if bottom_lines:
            return bottom_lines
        return False

    def has_leftmost_line(self):
        """ checks to see if there is a vertical line at the leftmost edge of the figure,
        and if so, returns True (otherwise returns False)
        :return: bool
        """
        vertical_lines = [line for line in self.lines if line.is_vertical()]
        leftmost_lines = [line for line in vertical_lines if line.start_point.x == self.get_lowest_x_coord()]
        if leftmost_lines:
            return leftmost_lines
        return False

    def align_with_frame_top(self):
        """ checks if it is possible to align the figure with the associated frame's
        top line, and if so, shifts the figure to the frame's top and returns True
        (otherwise returns False)
        :return: bool
        """
        top_lines = self.has_top_line()
        if not self.locked_y and top_lines:
            y_shift = self.frame.top_line.start_point.y - self.get_highest_y_coord()
            self.shift(x_shift=0, y_shift=y_shift)
            self.locked_y = True
            for line in top_lines:
                line.extended = True
            return True
        return False

    def align_with_frame_right(self):
        """ checks if it is possible to align the figure with the associated frame's
        rightmost line, and if so, shifts the figure to the frame's rightmost edge and
        returns True (otherwise returns False)
        :return: bool
        """
        right_lines = self.has_rightmost_line()
        if not self.locked_x and right_lines:
            x_shift = self.frame.right_line.start_point.x - self.get_highest_x_coord()
            self.shift(x_shift=x_shift, y_shift=0)
            self.locked_x = True
            for line in right_lines:
                line.extended = True
            return True
        return False

    def align_with_frame_bottom(self):
        """ checks if it is possible to align the figure with the associated frame's
        bottom line, and if so, shifts the figure to the frame's bottom and returns True
        (otherwise returns False)
        :return: bool
        """
        bottom_lines = self.has_bottom_line()
        if not self.locked_y and bottom_lines:
            y_shift = self.frame.bottom_line.start_point.y - self.get_lowest_y_coord()
            self.shift(x_shift=0, y_shift=y_shift)
            self.locked_y = True
            for line in bottom_lines:
                line.extended = True
            return True
        return False

    def align_with_frame_left(self):
        """ checks if it is possible to align the figure with the associated frame's
        leftmost line, and if so, shifts the figure to the frame's leftmost edge and
        returns True (otherwise returns False)
        :return: bool
        """
        left_lines = self.has_leftmost_line()
        if not self.locked_x and left_lines:
            x_shift = self.frame.left_line.start_point.x - self.get_lowest_x_coord()
            self.shift(x_shift=x_shift, y_shift=0)
            self.locked_x = True
            for line in left_lines:
                line.extended = True
            return True
        return False

    def align_with_frame(self):
        """ checks if it is possible to align the figure with one of the associated
        frame's lines/sides (checking them in a random order) and if so, shifts the
        figure so that it is aligned with the frame and returns True (otherwise
        returns False)
        :return: bool
        """
        align_functions = [self.align_with_frame_top, self.align_with_frame_right,
                           self.align_with_frame_bottom, self.align_with_frame_left]
        random.shuffle(align_functions)
        for align_fn in align_functions:
            if align_fn():
                return True
        return False

    def get_top_point(self):
        """ checks if there is one single point at the top of the figure,
        and if so, returns that point (otherwise returns False)
        :return: Point or bool
        """
        top_points = [point for point in self.unique_points if point.y == self.get_highest_y_coord()]
        if len(top_points) == 1:
            return top_points[0]
        return False

    def get_rightmost_point(self):
        """ checks if there is one single point at the rightmost edge of the figure,
        and if so, returns that point (otherwise returns False)
        :return: Point or bool
        """
        right_points = [point for point in self.unique_points if point.x == self.get_highest_x_coord()]
        if len(right_points) == 1:
            return right_points[0]
        return False

    def get_bottom_point(self):
        """ checks if there is one single point at the bottom of the figure,
        and if so, returns that point (otherwise returns False)
        :return: Point or bool
        """
        bottom_points = [point for point in self.unique_points if point.y == self.get_lowest_y_coord()]
        if len(bottom_points) == 1:
            return bottom_points[0]
        return False

    def get_leftmost_point(self):
        """ checks if there is one single point at the leftmost edge of the figure,
        and if so, returns that point (otherwise returns False)
        :return: Point or bool
        """
        left_points = [point for point in self.unique_points if point.x == self.get_lowest_x_coord()]
        if len(left_points) == 1:
            return left_points[0]
        return False

    def shift_to_frame_top(self):
        """ if the figure is not y-locked in place and has a lone top point, shift the figure
        to the top side of the associated frame and return True (otherwise return False)
        :return: bool
        """
        top_point = self.get_top_point()
        if top_point and not self.locked_y:
            self.shift(x_shift=0, y_shift=self.frame.top_line.start_point.y - self.get_highest_y_coord())
            return True
        return False

    def shift_to_frame_right(self):
        """ if the figure is not x-locked in place and has a lone rightmost point, shift the figure
        to the right side of the associated frame and return True (otherwise return False)
        :return: bool
        """
        right_point = self.get_rightmost_point()
        if right_point and not self.locked_x:
            self.shift(x_shift=self.frame.right_line.start_point.x - self.get_highest_x_coord(), y_shift=0)
            return True
        return False

    def shift_to_frame_bottom(self):
        """ if the figure is not y-locked in place and has a lone bottom point, shift the figure
        to the bottom side of the associated frame and return True (otherwise return False)
        :return: bool
        """
        bottom_point = self.get_bottom_point()
        if bottom_point and not self.locked_y:
            self.shift(x_shift=0, y_shift=self.frame.bottom_line.start_point.y - self.get_lowest_y_coord())
            return True
        return False

    def shift_to_frame_left(self):
        """ if the figure is not x-locked in place and has a lone leftmost point, shift the figure
        to the left side of the associated frame and return True (otherwise return False)
        :return: bool
        """
        left_point = self.get_leftmost_point()
        if left_point and not self.locked_x:
            self.shift(x_shift=self.frame.left_line.start_point.x - self.get_lowest_x_coord(), y_shift=0)
            return True
        return False

    def shift_to_frame(self):
        """ if the figure is not x- and y-locked in place and has a lone point at a border, shift the figure
        to a side (chosen randomly from the possible sides) of the associated frame and return True
        (otherwise return False)
        :return: bool
        """
        shift_functions = [self.shift_to_frame_top, self.shift_to_frame_right,
                           self.shift_to_frame_bottom, self.shift_to_frame_left]
        random.shuffle(shift_functions)
        for shift_fn in shift_functions:
            result = shift_fn()
            if result:
                return True
        return False

    def extend_line(self):
        """extend a random figure line so that it runs all the way to the passed frame's sides
        and return True, unless all lines are already extended (in that case return False)
        :return: bool"""
        shuffled_lines = random.sample(self.lines, k=len(self.lines))
        for line in shuffled_lines:
            if line.extend(self.frame):
                return True
        return False

    def randomly_position(self):
        """randomly positions the figure somewhere within the frame and returns True, or returns
        False if the figure is x- or y-locked in place. the figure is placed at least 50 units
        away from each side of the frame
        :return: bool"""
        if self.locked_x or self.locked_y:
            return False
        max_shift_x = self.frame.right_line.start_point.x - self.get_highest_x_coord() - 15
        min_shift_x = self.frame.left_line.start_point.x - self.get_lowest_x_coord() + 15
        max_shift_y = self.frame.top_line.start_point.y - self.get_highest_y_coord() - 15
        min_shift_y = self.frame.bottom_line.start_point.y - self.get_lowest_y_coord() + 15
        x_shift = random.uniform(min_shift_x, max_shift_x)
        y_shift = random.uniform(min_shift_y, max_shift_y)
        self.shift(x_shift=x_shift, y_shift=y_shift)
        return True

    def grow_line(self, orientation):
        """grow a line with the specified orientation from one of the figure's points
        that runs between two of the passed frame's sides and return it, if a line hasn't already
        been grown from all the figure's points (in that case return False)
        :param orientation: "horizontal", "vertical" or "diagonal"
        :type orientation: string
        :return: AttachedLine or bool"""
        randomly_ordered_points = random.sample(self.unique_points, len(self.unique_points))
        for point in randomly_ordered_points:
            line_or_false = point.grow_line(frame=self.frame, orientation=orientation)
            if line_or_false:
                return line_or_false
        return False

    def find_free_points(self):
        """finds all points in the figure that are loose ends, i. e. that aren't part of two figure lines and
        are more than 3 units away from all other figure points
        :return: list of Point objects"""
        free_points = []
        for point_index in range(len(self.all_points)):
            curr_point = self.all_points[point_index]
            if curr_point.grown:
                continue
            if curr_point.x in [self.frame.left_line.start_point.x, self.frame.right_line.start_point.x]:
                continue
            if curr_point.y in [self.frame.top_line.start_point.y, self.frame.bottom_line.start_point.y]:
                continue
            set_without_curr_point = set([point for i, point in enumerate(self.all_points) if i != point_index])
            if curr_point in set_without_curr_point:
                continue
            related_line = [line for line in self.lines if curr_point in [line.start_point, line.end_point]][0]
            if related_line.extended:
                continue
            has_nearby_point = False
            for compare_point in set_without_curr_point:
                if curr_point.dist(compare_point) < 3:
                    has_nearby_point = True
                    break
            if not has_nearby_point:
                free_points.append(curr_point)
        return free_points

    def close_up_free_points(self):
        if self.closed:
            return []
        free_points = self.find_free_points()
        grown_lines = []
        for point in free_points:
            orientation = random.choice(["horizontal", "vertical", "diagonal", "diagonal"])
            grown_lines.append(point.grow_line(frame=self.frame, orientation=orientation))
        self.closed = True
        return grown_lines
