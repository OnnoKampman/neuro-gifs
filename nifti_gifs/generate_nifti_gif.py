import os

from matplotlib.cm import get_cmap
import numpy as np

from nifti_gifs.file_helpers import save_gif, process_image

mode = 'normal'


def generate_gif(filename: str, size=1, frames_per_second: int = 18, colormap=None) -> None:
    """
    Creates and saves a NifTi image mosaic gif.
    :param filename: input file name (should end with .nii)
    :param size: size of the gif, between 0 and 1
    :param frames_per_second:
    :param colormap: cmaps are taken from matplotlib
    """
    out_img, maximum = process_image(filename, size)
    new_img = create_standard_mosaic(out_img, maximum)

    if colormap is not None:
        # Transform values according to the color map
        cmap = get_cmap(colormap)
        color_transformed = [cmap(new_img[i, ...]) for i in range(maximum)]
        cmap_img = np.delete(color_transformed, 3, 3)
        new_img = cmap_img
    else:
        colormap = 'grayscale'

    save_gif(
        filename.replace(os.path.splitext(filename)[1], '_%s.gif' % colormap),
        new_img,
        frames_per_second,
        size
    )

