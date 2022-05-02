"""
NOTE that for this script to work, you must first move it to the project's root directory ('one level up').

Example of how to use the package for generating a single L-EFT stimulus image,
where target 'C3' has been embedded in a context image. The `random` calls
ensure that certain aspects of the generation are pseudo-randomized.
"""
from leftstim.build import LeftImage
import random
import os

SAVE_DIR_NAME = "generated_images"

my_img = LeftImage(500, 500, 300, 300, background_color=(1, 1, 1), line_color=(-1, -1, -1), line_width=1.8, units="pix")
my_img.add_figure_by_name('C3')
my_img.randomly_position_figure()
should_attach = random.random() < 0.4
if should_attach:
    # attempt to move the figure so that one of its lines overlaps with
    # a 'frame' border
    my_img.align_figure_with_frame()
should_shift = random.random() < 0.4
if should_shift:
    # attempt to move the figure so that one of its points lies on a
    # frame border
    my_img.shift_figure_to_frame()
my_img.extend_two_thirds_figure_lines()
# 'C3' has some 'free ends', points only connected to by one line. this
# call ensures that these 'free ends' will be 'struck through' by a line
my_img.close_figure_free_points()

extra_lines_no = 5
# use a for loop to add 5 extra lines
for i in range(extra_lines_no):
    has_been_grown = False
    grow_line = True if random.random() < 0.2 else False
    if grow_line:
        # attempt to make one of the figure's lines 'grow', i.e. be
        # extended
        has_been_grown = my_img.grow_figure_line()
    if not has_been_grown:
        # if it's not the case that one of the figure's lines was extended,
        # add a random line with a random orientation
        orientation = random.choice(['horizontal', 'vertical', 'diagonal'])
        my_img.add_random_line(orientation)

if not os.path.isdir(SAVE_DIR_NAME):
    os.mkdir(SAVE_DIR_NAME)

my_img.save_image_and_context(os.path.join(os.getcwd(), SAVE_DIR_NAME))
