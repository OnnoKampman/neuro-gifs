import os

from matplotlib.cm import get_cmap
import numpy as np

from nifti_gifs.file_helpers import save_gif, process_image

mode = 'normal'


def create_standard_mosaic(out_img: np.array, maximum: int) -> np.array:
    """
    Creates grayscale image.
    """
    print('out_image', out_img.shape)
    new_img = [
        np.hstack((
            np.hstack((
                np.flip(out_img[i, :, :], 1).T,
                np.flip(out_img[:, maximum - i - 1, :], 1).T)
            ),
            np.flip(out_img[:, :, maximum - i - 1], 1).T)
        ) for i in range(maximum)
    ]
    new_img = np.array(new_img)
    print('new_img', new_img.shape)
    return new_img


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

