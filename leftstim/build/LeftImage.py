from copy import deepcopy
import inspect
import math
import os
import random

from psychopy import visual

from leftstim.basic_components.AttachedLine import AttachedLine
from leftstim.basic_components.Line import Line
from leftstim.basic_components.Point import Point
from leftstim.complex_components.Frame import Frame
from leftstim.complex_components.Figure import Figure

from leftstim.original_targets.FigureLineCollections import FigureLineCollections

class LeftImage:
    def __init__(self, window_width, window_height,
                 frame_width, frame_height,
                 line_width, line_color,
                 background_color, units):
        self.non_fig_lines = []
        self.figure = None
        self.nonextended_figure = None
        self.figure_linked_lines = []
        self.window = visual.Window(size=(window_width, window_height),
                                    color=background_color, units=units)
        self.line_object = visual.Line(self.window, units=units,
                                       lineWidth=line_width, lineColor=line_color,
                                       lineColorSpace="rgb",
                                       start=(0, 0),
                                       end=(0, 0),
                                       opacity=1,
                                       interpolate=True)
        frame_top = Line(Point(-frame_width/2, frame_height/2), Point(frame_width/2, frame_height/2))
        frame_right = Line(Point(frame_width/2, frame_height/2), Point(frame_width/2, -frame_height/2))
        self.frame = Frame(frame_top, frame_right)

    def add_figure(self, figure):
        """set the image's figure. there may only be one. its frame will be set to this Image
        instance's frame, if it was a different one.
        :type figure: Figure"""
        figure.frame = self.frame
        self.figure = figure
        self.nonextended_figure = deepcopy(figure)

    def add_random_figure(self):
        fig_name, line_collection = FigureLineCollections.grab_random_collection()
        rand_fig = Figure(line_collection, self.frame)
        rand_fig.figure_name = fig_name
        self.add_figure(rand_fig)

    def add_figure_by_name(self, figure_name):
        assert figure_name in FigureLineCollections.all_line_collections.keys(), "Please specify a valid figure " \
                                                                                   "name, in the format <[A-D][1-4]>"
        named_fig = Figure(FigureLineCollections.all_line_collections[figure_name], self.frame)
        named_fig.figure_name = figure_name
        self.add_figure(named_fig)

    def randomly_position_figure(self):
        if self.figure is None:
            return False
        self.figure.randomly_position()
        self.nonextended_figure = deepcopy(self.figure)
        return True

    def extend_figure_line(self):
        if self.figure is None:
            return False
        if self.figure.extend_line():
            return True
        return False

    def extend_all_figure_lines(self):
        if self.figure is None:
            return False
        extended = True
        count = -1
        while extended:
            extended = self.extend_figure_line()
            count += 1
        if count > 0:
            return True
        return False

    def extend_two_thirds_figure_lines(self):
        if self.figure is None:
            return False
        count = -1
        already_extended_fig_lines = [line for line in self.figure.lines if line.extended]
        num_to_extend = math.ceil(len(self.figure.lines)*2/3) - len(already_extended_fig_lines)
        if num_to_extend < 1:
            return False
        for i in range(num_to_extend):
            extended = self.extend_figure_line()
            count += 1
            if not extended:
                break
        if count > 0:
            return True
        return False

    def align_figure_with_frame(self):
        if self.figure is None:
            return False
        self.figure.align_with_frame()
        self.nonextended_figure = deepcopy(self.figure)

    def shift_figure_to_frame(self):
        if self.figure is None:
            return False
        res = self.figure.shift_to_frame()
        self.nonextended_figure = deepcopy(self.figure)
        return res

    def add_side2side_line(self, orientation):
        """add a line to the image that runs from one of the frame's sides
         to another side, with specified orientation"""
        already_existing_lines = self.get_all_lines()
        too_close = True
        while too_close:
            too_close = False
            new_line_candidate = self.frame.fling_side_to_side(orientation=orientation)
            for line in already_existing_lines:
                if line.get_max_dist(new_line_candidate) < 40:
                    too_close = True
                    break
        self.non_fig_lines.append(new_line_candidate)

    def add_side2line_line(self, orientation):
        """add a line, with specified orientation, to the image that runs from one of the frame's sides
         to a randomly chosen non-frame line (returns False if there is no
         figure and no other non-frame lines)"""
        if len(self.non_fig_lines) < 1 and self.figure is None:
            return False
        if self.figure is None:
            start_line = random.choice(self.non_fig_lines)
            self.non_fig_lines.append(self.frame.fling_side_to_line(start_line=start_line,
                                                                     orientation=orientation))
        else:
            start_line = random.choice(self.figure.lines + self.non_fig_lines)
            if start_line in self.figure.lines:
                self.figure_linked_lines.append(self.frame.fling_side_to_line(start_line=start_line,
                                                                               orientation=orientation))
            else:
                self.non_fig_lines.append(self.frame.fling_side_to_line(start_line=start_line,
                                                                         orientation=orientation))

    def add_line2line_line(self):
        """add a line to the image that runs between two non-frame lines, if at least two non-frame lines exist"""
        if len(self.non_fig_lines) < 2 and (self.figure is None or len(self.non_fig_lines) < 1):
            return False
        if self.figure is None:
            start_line, end_line = random.sample(self.non_fig_lines, 2)
            self.non_fig_lines.append(start_line.fling_to_line(end_line))
        else:
            all_lines = self.figure.lines + self.non_fig_lines
            start_line = random.choice(all_lines)
            end_line = random.choice(self.non_fig_lines)
            if start_line in self.figure.lines or end_line in self.figure.lines:
                self.figure_linked_lines.append(start_line.fling_to_line(end_line))
            else:
                self.non_fig_lines.append(start_line.fling_to_line(end_line))

    def add_random_line(self, orientation='diagonal'):
        """add a random line. the different kinds of lines are weighted, so that
        frame-to-frame lines are more likely than frame-to-inside-line, and
        inside-line-to-inside-line lines are even less likely. orientation is specified
        as orientation argument, otherwise 'diagonal' orientation is assumed."""
        line_funcs = [
            self.add_side2side_line, self.add_side2side_line,
            self.add_side2side_line, self.add_side2side_line,
            self.add_side2side_line, self.add_line2line_line,
            self.add_side2line_line, self.add_side2line_line
        ]
        line_added = False
        while not line_added:
            try:
                line_func = random.choice(line_funcs)
                if 'orientation' in inspect.getfullargspec(line_func).args:
                    line_func(orientation)
                else:
                    line_func()
                line_added = True
            except AttributeError as e:
                print(e)
                print('trying to add random line again...')

    def draw(self):
        """draw all the elements in the Image instance"""
        self.frame.draw(self.window, self.line_object)
        if self.figure is not None:
            for line in self.figure.lines:
                if line.is_horizontal() and line.start_point.y in \
                        (self.frame.top_line.start_point.y, self.frame.bottom_line.start_point.y):
                    continue
                elif line.is_vertical() and line.start_point.x in \
                        (self.frame.left_line.start_point.x, self.frame.right_line.start_point.x):
                    continue
                line.draw(self.window, self.line_object)
        for line in self.non_fig_lines:
            if line.is_horizontal() and line.start_point.y in \
                    (self.frame.top_line.start_point.y, self.frame.bottom_line.start_point.y):
                continue
            elif line.is_vertical() and line.start_point.x in \
                    (self.frame.left_line.start_point.x, self.frame.right_line.start_point.x):
                continue
            line.draw(self.window, self.line_object)
        for line in self.figure_linked_lines:
            line.draw(self.window, self.line_object)

    def draw_just_figure(self):
        """draw all the elements in the Image instance"""
        self.frame.draw(self.window, self.line_object)
        if self.figure is not None:
            for line in self.nonextended_figure.lines:
                if line.is_horizontal() and line.start_point.y in \
                        (self.frame.top_line.start_point.y, self.frame.bottom_line.start_point.y):
                    continue
                elif line.is_vertical() and line.start_point.x in \
                        (self.frame.left_line.start_point.x, self.frame.right_line.start_point.x):
                    continue
                line.draw(self.window, self.line_object)

    def get_all_lines(self):
        if self.figure is None:
            return self.non_fig_lines + self.figure_linked_lines
        return self.figure.lines + self.non_fig_lines + self.figure_linked_lines

    def jiggle_non_fig_lines(self):
        for line in self.non_fig_lines:
            line.jiggle_all()

    def replace_figure_with_lines(self):
        """remove the image's figure and replace it with random lines"""
        assert self.figure is not None, "the Image instance must include a figure in order to use " \
                                         "draw_without_figure()"
        assert len(self.get_all_lines()) > 5, "Image instance must hold a minimum of 6 lines before replacing figure"
        extended_lines = [line.get_extended_version(self.frame) for line in self.figure.lines + self.figure_linked_lines]
        num_non_extended_fig_lines = sum([line.extended for line in self.figure.lines])
        self.figure = None
        self.figure_linked_lines = []
        num_to_jiggle = random.randint(len(extended_lines)//3, len(extended_lines)//3*2)
        num_not_to_jiggle = len(extended_lines)-num_to_jiggle
        num_to_leave_alone = random.randint(num_not_to_jiggle//3, num_not_to_jiggle//3*2)
        num_to_replace = len(extended_lines) - num_to_jiggle - num_to_leave_alone

        jiggle_lines = random.sample(extended_lines, num_to_jiggle)
        non_jiggle_lines = set(extended_lines) - set(jiggle_lines)
        leave_alone_lines = random.sample(non_jiggle_lines, num_to_leave_alone)
        to_be_replaced_lines = set(extended_lines) - set(jiggle_lines) - set(leave_alone_lines)

        for line in jiggle_lines:
            line.jiggle_all()
            self.non_fig_lines.append(line)

        self.non_fig_lines.extend(leave_alone_lines)

        for line in to_be_replaced_lines:
            orientation = line.get_orientation()
            if num_non_extended_fig_lines > 0:
                add_fun = random.choice(["line2line", "side2line"])
                if add_fun == "line2line":
                    self.add_line2line_line()
                else:
                    self.add_side2side_line(orientation)
                num_non_extended_fig_lines -= 1
            else:
                self.add_random_line(orientation=orientation)

        all_lines_after_transform = self.get_all_lines()
        for line in all_lines_after_transform:
            if isinstance(line, AttachedLine):
                line.extend_to_parents(self.frame)

    def close_figure_free_points(self):
        if self.figure is None:
            return False
        grown_lines = self.figure.close_up_free_points()
        self.non_fig_lines.extend(grown_lines)

    def grow_figure_line(self):
        if self.figure is None:
            return False
        orientation = random.choice(["horizontal", "vertical", "diagonal", "diagonal"])
        grown_line = self.figure.grow_line(orientation=orientation)
        if grown_line:
            self.non_fig_lines.append(grown_line)
            return True
        return False

    def save_image(self, file_dir):
        """draw and save the image to the specified file directory"""
        if self.figure is None:
            file_path = os.path.join(file_dir, "no_figure_" + str(random.randint(1, 20000)) + ".png")
        else:
            file_path = os.path.join(file_dir, self.figure.figure_name + "_" + str(random.randint(1, 20000)) + ".png")
        self.draw()
        self.window.flip()
        self.window.getMovieFrame()
        self.window.saveMovieFrames(fileName=file_path)

    def save_image_and_context(self, file_dir):
        """draw and save the image, a context image where the figure has been replaced with
        random lines, and an image where only the figure/target is included,
        to the specified file directory
        """
        assert self.figure is not None, "the Image instance must include a figure in order to use " \
                                         "save_image_and_contexts()"
        file_no = str(random.randint(1, 20000))
        file_path = os.path.join(
            file_dir,
            self.figure.figure_name + "_" +
                file_no + "_onlyfigure.png"
        )
        self.draw_just_figure()
        self.window.flip()
        self.window.getMovieFrame()
        self.window.saveMovieFrames(fileName=file_path)
        file_path = os.path.join(
            file_dir,
            self.figure.figure_name + "_" +
                file_no + "_embeddedfigure.png"
        )
        self.draw()
        self.window.flip()
        self.window.getMovieFrame()
        self.window.saveMovieFrames(fileName=file_path)
        file_path = os.path.join(
            file_dir,
            self.figure.figure_name + "_" +
                file_no + "_nofigure.png"
        )
        self.jiggle_non_fig_lines()
        self.replace_figure_with_lines()
        self.draw()
        self.window.flip()
        self.window.getMovieFrame()
        self.window.saveMovieFrames(fileName=file_path)
        self.window.close()
