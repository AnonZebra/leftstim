"""
Example of how to use the package for generating a single L-EFT stimulus image,
where target 'A2' has been embedded in a context image.
"""
from leftstim.build import LeftImage
import os

SAVE_DIR_NAME = "generated_images"

# start creating image, with:
# * white background color and black line color.
# * total image size of 500x500 pixels
# * 'frame' in which all lines will be placed of size 300x300 pixels
#   (i.e. with 'margins' that are 100px wide in on all sides)
my_img = LeftImage(500, 500, 300, 300, background_color=(1, 1, 1), line_color=(-1, -1, -1), line_width=1.8, units="pix")
# target names are 'A1', 'A2', 'A3', 'A4', 'B1', 'B2'... 'D3', 'D4'.
# select 'A2' here.
my_img.add_figure_by_name('A2')
my_img.randomly_position_figure()
# make two thirds (as closely as possible) of the figure's lines extend
# to the frame's borders
my_img.extend_two_thirds_figure_lines()

# add some random lines
my_img.add_random_line(orientation='horizontal')
my_img.add_random_line(orientation='horizontal')
my_img.add_random_line(orientation='vertical')
my_img.add_random_line(orientation='diagonal')

# if the directory to save images to doesn't yet exist, create it
if not os.path.isdir(SAVE_DIR_NAME):
    os.mkdir(SAVE_DIR_NAME)

# save the resulting image, as well as an alternate version where only the figure
# is shown, and another alternate version where the figure has been replaced by
# random lines and the remaining lines have been slightly shifted
my_img.save_image_and_context(os.path.join(os.getcwd(), SAVE_DIR_NAME))

# check the 'generated_images' directory to see the results