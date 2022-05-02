from leftstim.basic_components.Point import Point
from leftstim.basic_components.Line import Line

class AttachedLine(Line):
    def __init__(self, start_point, end_point, start_line, end_line):
        """generate AttachedLine instance that represents a non-curved line in 2D space, connected
        at its ends to other lines
        :param start_line: line connected to start of this line
        :type start_line: Line
        :param end_line: line connected to end of this line
        :type end_line: Line
        :return: None"""
        super().__init__(start_point, end_point)
        self.start_line = start_line
        self.end_line = end_line

    def change_start_line(self, new_start_point, new_start_line):
        """change this line's starting point, attaching to the specified new start line

        :param new_start_point: new starting point
        :type new_start_point: Point
        :param new_start_line: new line for start of this line to attach to
        :type new_start_line: Line
        :return: None
        """
        self.start_point = new_start_point
        self.start_line = new_start_line

    def change_end_line(self, new_end_point, new_end_line):
        """change this line's end point, attaching to the specified new start line

        :param new_end_point: new end point
        :type new_end_point: Point
        :param new_end_line: new line for end of this line to attach to
        :type new_end_line: Line
        :return: None
        """
        self.start_point = new_end_point
        self.start_line = new_end_line

    def jiggle_start(self):
        """randomly change this line's starting point, while forcing it to stay on the line
        attached to the start of this line
        :return: None"""
        self.start_point = self.get_jiggle_line_start().get_random_point()

    def jiggle_end(self):
        """randomly change this line's end point, while forcing it to stay on the line
        attached to the end of this line
        :return: None"""
        self.end_point = self.get_jiggle_line_end().get_random_point()

    def jiggle_all(self):
        """randomly change this line's start and end point, while forcing them to stay on the lines
        attached to the start/end of this line, respectively. takes into account what orientation
        the line originally had.
        :return: None"""
        orientation = self.get_orientation()
        try:
            self.jiggle_start()
            if orientation == "horizontal":
                horizontal_line = Line(self.start_point, self.start_point + Point(1, 0))
                inter_point = horizontal_line.get_intersection(self.end_line)
                self.end_point = inter_point
            elif orientation == "vertical":
                vertical_line = Line(self.start_point, self.start_point + Point(0, 1))
                inter_point = vertical_line.get_intersection(self.end_line)
                self.end_point = inter_point
            else:
                self.jiggle_end()
        except AttributeError as e:
            print(e)
            print('skipping jiggling line')


    def get_jiggle_line_start(self):
        """generates a Line object to be used when jiggling"""
        diff_start = self.start_point - self.start_line.start_point
        diff_end = self.start_point - self.start_line.end_point
        start_point = self.start_point - diff_start/3
        end_point = self.start_point - diff_end/3
        return Line(start_point, end_point)

    def get_jiggle_line_end(self):
        """generates a Line object to be used when jiggling"""
        diff_start = self.end_point - self.end_line.start_point
        diff_end = self.end_point - self.end_line.end_point
        start_point = self.end_point - diff_start/3
        end_point = self.end_point - diff_end/3
        return Line(start_point, end_point)

    def shift(self, x_shift, y_shift):
        """method that overrides parent method to ensure it isn't used"""
        raise Exception("This is an AttachedLine instance. Shift should not be used with AttachedLine instances. "
                        "Please use the .change_start_line() and .change_end.line() methods instead.")

    def extend_to_parents(self, frame):
        """extends the attached line so that it touches the start_line and end_line, if possible. if the
        resulting line reaches outside of the frame, or it's not possible to extend to start/end_lines,
        replace this line with a random line running between the start_line and end_line"""
        extension_successful = False
        try:
            start_point = self.get_intersection(self.start_line)
            end_point = self.get_intersection(self.end_line)
            if start_point.is_in_frame(frame) and end_point.is_in_frame(frame):
                self.start_point = start_point
                self.end_point = end_point
                extension_successful = True
        except AttributeError as e:
            print(e)
            print('Unable to extend line, replacing with random line...')
        finally:
            if not extension_successful:
                self.start_point = self.start_line.get_random_point()
                self.end_point = self.end_line.get_random_point()

