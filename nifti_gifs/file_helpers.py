from imageio import mimwrite
import numpy as np


def save_gif(filename: str, gif_array: np.array, frames_per_second: int, resize_factor) -> None:
    mimwrite(
        filename,
        gif_array,
        format='gif',
        fps=int(frames_per_second * resize_factor)
    )
    print("Gif saved in %s" % filename)
