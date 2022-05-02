from leftstim.basic_components.Point import Point
from leftstim.basic_components.Line import Line
from leftstim.basic_components.AttachedLine import AttachedLine

class FigureLine(Line):
    extended = False

    def __init__(self, start_point, end_point):
        """generate FigureLine instance that represents a non-curved line in 2D space, that
        is part of a figure"""
        super().__init__(start_point, end_point)
        self.start_ext_point = start_point
        self.end_ext_point = end_point

    def extend(self, frame):
        """extend the line so that it runs all the way to the passed frame's sides and return True,
        if it isn't already extended (in that case return False)
        :param frame: frame to extend the line to
        :type frame: Frame
        :return: bool"""
        if self.extended:
            return False
        frame_top_y = frame.top_line.start_point.y
        frame_right_x = frame.right_line.start_point.x
        frame_bottom_y = frame.bottom_line.start_point.y
        frame_left_x = frame.left_line.start_point.x
        if self.is_horizontal():
            self.end_ext_point = Point(frame_right_x, self.end_ext_point.y)
            self.start_ext_point = Point(frame_left_x, self.start_ext_point.y)
        elif self.is_vertical():
            self.end_ext_point = Point(self.end_ext_point.x, frame_top_y)
            self.start_ext_point = Point(self.start_ext_point.x, frame_bottom_y)
        else:
            if self.end_point.x > self.start_point.x:
                leftmost_point, rightmost_point = self.start_point, self.end_point
            else:
                leftmost_point, rightmost_point = self.end_point, self.start_point
            line_k = (rightmost_point.y - leftmost_point.y) / (rightmost_point.x - leftmost_point.x)
            if line_k < 0 and abs((frame_right_x-leftmost_point.x) * line_k) < abs(leftmost_point.y-frame_bottom_y):
                new_y = (frame_right_x-leftmost_point.x) * line_k + leftmost_point.y
                new_x = frame_right_x
                self.end_ext_point = Point(new_x, new_y)
            elif line_k < 0:
                new_y = frame_bottom_y
                new_x = (frame_bottom_y - leftmost_point.y)/line_k + leftmost_point.x
                self.end_ext_point = Point(new_x, new_y)
            elif abs((frame_right_x-leftmost_point.x) * line_k) < abs(frame_top_y - leftmost_point.y):
                new_y = (frame_right_x-leftmost_point.x) * line_k + leftmost_point.y
                new_x = frame_right_x
                self.end_ext_point = Point(new_x, new_y)
            else:
                new_y = frame_top_y
                new_x = (frame_top_y - leftmost_point.y)/line_k + leftmost_point.x
                self.end_ext_point = Point(new_x, new_y)
            if line_k < 0 and abs((frame_left_x-leftmost_point.x) * line_k) < abs(frame_top_y - leftmost_point.y):
                new_y = (frame_left_x-leftmost_point.x) * line_k + leftmost_point.y
                new_x = frame_left_x
                self.start_ext_point = Point(new_x, new_y)
            elif line_k < 0:
                new_y = frame_top_y
                new_x = (frame_top_y - leftmost_point.y)/line_k + leftmost_point.x
                self.start_ext_point = Point(new_x, new_y)
            elif abs((frame_left_x-leftmost_point.x) * line_k) < abs(leftmost_point.y - frame_bottom_y):
                new_y = (frame_left_x-leftmost_point.x) * line_k + leftmost_point.y
                new_x = frame_left_x
                self.start_ext_point = Point(new_x, new_y)
            else:
                new_y = frame_bottom_y
                new_x = -(leftmost_point.y - frame_bottom_y)/line_k + leftmost_point.x
                self.start_ext_point = Point(new_x, new_y)
        self.extended = True
        return True

    def draw(self, window, line_object):
        """overrides parent Line method. draws the line (using the extended points)
        in a specified window using a specified line object
        :param window: PsychoPy window to draw in
        :type window: psychopy.visual.Window
        :param line_object: PsychoPy line instance to draw with
        :type line_object: psychopy.visual.Line
        :return: None"""
        line_object.start = (self.start_ext_point.x, self.start_ext_point.y)
        line_object.end = (self.end_ext_point.x, self.end_ext_point.y)
        line_object.draw()
