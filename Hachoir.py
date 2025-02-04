# Hachoir.py
# auteur: Denis-Carl Robidoux (2024) pour le MEM
#
# License: General Public
#
###
import sys, glob, os
from PIL import Image, ImageDraw

layout = [
    (96, 14),
    (96, 14),
    (96, 14),
    (74, 24),
    (48, 14),
    (96, 14),
    (96, 14),
    (97, 0)
]

class Hachoir:
    def __init__(self, fnIn, fnOut):
        self.image=Image.open(fnIn)
        posFrom = 0
        posTo = 0
        lastWin = None
        for window in layout:
            if lastWin is None:
                lastWin = window
                continue
            posFrom += lastWin[0] + lastWin[1]
            posTo += lastWin[0]
            self.copy_and_paste((posFrom, 0), (posTo, 0), (window[0], 180))
            lastWin = window
        draw = ImageDraw.Draw(self.image)
        draw.line((362, 0, 362, 180), fill="black", width=1)
        finalCrop=self.image.crop((0,0,699,180))
        finalCrop.save(fnOut, quality=98, subsampling=0)

    def copy_and_paste(self, from_coords: tuple, to_coords: tuple, area_size: tuple):
        cropped_area = self.image.crop((from_coords[0], from_coords[1],
                                        from_coords[0]+area_size[0],
                                        from_coords[1]+area_size[1]))
        self.image.paste(cropped_area, to_coords)
        return self.image

if __name__ == "__main__":
    pattern = sys.argv[1]
    outdir = sys.argv[2]
    for fn in glob.glob(pattern):
        basename = os.path.basename(fn)
        outpath = os.path.join(outdir, basename)
        Hachoir(fn, outpath)
