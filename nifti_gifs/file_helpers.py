import os

from imageio import mimwrite
import nibabel as nb
import numpy as np
from skimage.transform import resize


def save_gif(filename: str, gif_array: np.array, frames_per_second: int, resize_factor: float) -> None:
    mimwrite(
        filename,
        gif_array,
        format='gif',
        fps=int(frames_per_second * resize_factor)
    )
    print("Gif saved in %s" % filename)


def load_data(filename: str) -> np.array:
    data = nb.load(filename).get_data()
    print('data', data.shape)
    return data

