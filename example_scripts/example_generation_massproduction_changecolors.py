"""
NOTE that for this script to work, you must first move it to the project's root directory ('one level up').

Example of how to generate large number of image sets.
"""
import os
import random

from leftstim.build import LeftImage

SAVE_DIR_NAME = "generated_images"
NUM_SETS = 30

if not os.path.isdir(SAVE_DIR_NAME):
    os.mkdir(SAVE_DIR_NAME)

# use a for loop to generate as many image sets as desired
for i in range(NUM_SETS):
    print(i)
    # set background color to grey, and line color to orange
    my_img = LeftImage(500, 500, 300, 300, background_color=(0, 0, 0), line_color=(1, 0.3, -0.5), line_width=1.8, units="pix")
    # randomly select which figure to embed
    figure_type = random.choice(['A', 'B', 'C', 'D'])
    figure_number = random.choice(['1', '2', '3', '4'])
    figure_id = figure_type + figure_number
    my_img.add_figure_by_name(figure_id)
    my_img.randomly_position_figure()
    my_img.extend_two_thirds_figure_lines()
    extra_lines_no = 5
    for i in range(extra_lines_no):
        has_been_grown = False
        grow_line = True if random.random() < 0.2 else False
        if grow_line:
            has_been_grown = my_img.grow_figure_line()
        if not has_been_grown:
            orientation = random.choice(['horizontal', 'vertical', 'diagonal'])
            my_img.add_random_line(orientation)
    my_img.save_image_and_context(os.path.join(os.getcwd(), SAVE_DIR_NAME))
    print('DONE\n\n\n')
