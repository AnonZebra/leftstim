import random

from leftstim.basic_components.AttachedLine import AttachedLine
from leftstim.basic_components.Line import Line
from leftstim.basic_components.Point import Point

class Frame:
    def __init__(self, top_line, right_line):
        """generate a Frame instance that represents a rectangular frame in 2D space
        :param top_line: line representing top of frame
        :type top_line: Line
        :param right_line: line representing right border of frame
        :type right_line: Line
        """
        self.width = abs(top_line.end_point.x - top_line.start_point.x)
        self.height = abs(right_line.end_point.y - right_line.start_point.y)
        self.top_line = top_line
        self.right_line = right_line
        self.bottom_line = Line(top_line.start_point + Point(x=0, y=-self.height),
                                top_line.end_point + Point(x=0, y=-self.height))
        self.left_line = Line(right_line.start_point + Point(x=-self.width, y=0),
                              right_line.end_point + Point(x=-self.width, y=0))
        self.lines = [self.top_line, self.right_line, self.bottom_line, self.left_line]

    def draw(self, window, line_object):
        """draws the frame in a specified window using a specified line object
        :param window: PsychoPy window to draw in
        :type window: psychopy.visual.Window
        :param line_object: PsychoPy line instance to draw with
        :type line_object: psychopy.visual.Line
        :return: None"""
        for line in self.lines:
            line.draw(window, line_object)

    def fling_side_to_side(self, orientation):
        """ generate an AttachedLine instance that stretches from one of this frame's sides to another of its sides
        :param orientation: specification of the generated line's orientation. one of "horizontal" / "vertical" /
        "diagonal"
        :type orientation: str
        :return: AttachedLine
        """
        if orientation == "vertical":
            start_point = self.top_line.get_random_point()
            end_point = start_point - Point(x=0, y=self.height)
            start_line = self.top_line
            end_line = self.bottom_line
        elif orientation == "horizontal":
            start_point = self.right_line.get_random_point()
            end_point = start_point - Point(x=self.width, y=0)
            start_line = self.right_line
            end_line = self.left_line
        else:
            start_line = random.choice(self.lines)
            end_line = random.choice([line for line in self.lines if line is not start_line])
            return start_line.fling_to_line(end_line)
        return AttachedLine(start_point=start_point, end_point=end_point,
                            start_line=start_line, end_line=end_line)

    def fling_side_to_line(self, start_line, orientation):
        """ generate an AttachedLine instance that stretches from specified line to one of this frame's sides
        :param start_line: specified start line
        :type start_line: Line
        :param orientation: specification of the generated line's orientation. one of "horizontal" / "vertical" /
        "diagonal"
        :type orientation: str
        :return: AttachedLine
        """
        distant_enough = False
        counter = 100
        while not distant_enough:
            if counter <= 0:
                raise AttributeError("tried to fling to a line that is too close")
            start_point = start_line.get_random_point()
            if orientation == "vertical":
                end_line = random.choice((self.top_line, self.bottom_line))
                end_point = Point(end_line.start_point.x, start_point.y)
            elif orientation == "horizontal":
                end_line = random.choice((self.right_line, self.left_line))
                end_point = Point(start_point.x, end_line.start_point.y)
            else:
                end_line = random.choice(self.lines)
                end_point = end_line.get_random_point()
            if start_point.dist(end_point) > 50:
                distant_enough = True
            counter -= 1
        return AttachedLine(start_point=start_point, end_point=end_point,
                            start_line=start_line, end_line=end_line)

    def get_random_point(self):
        rand_line = random.choice(self.lines)
        return rand_line.get_random_point()
