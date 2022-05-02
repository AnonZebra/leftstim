import re

from leftstim.basic_components.Line import Line
from leftstim.basic_components.Point import Point

class ConversionFunctions:
    @staticmethod
    def translate_mathematica_coords(mathematica_str):
        """
        Original targets' coordinates were originally extracted by use of Mathematica.
        This function simply helps with converting the coordinates to a list of Line
        instances which correspond to the original targets' lines.
        """
        astr = mathematica_str
        re_patt_repl_dict = {"`": "", "{": "[", "}": "]"}
        for key in re_patt_repl_dict.keys():
            astr = re.sub(key, re_patt_repl_dict[key], astr)
        point_ls = eval(astr)
        point_ls = [Point(round(p[0]), round(p[1])) - Point(250, 250) for p in point_ls]
        line_ls = []
        for i in range(0, len(point_ls) - 1, 2):
            new_line = Line(point_ls[i], point_ls[i + 1])
            line_ls.append(new_line)
        return line_ls
