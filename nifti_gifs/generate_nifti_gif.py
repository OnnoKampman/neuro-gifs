import os

from imageio import mimwrite
from matplotlib.cm import get_cmap
import nibabel as nb
import numpy as np
from skimage.transform import resize


class NiftyGifGenerator:

    def __init__(self, file_path: str):
        """
        :param file_path: input file name (should end with .nii)
        """
        self.data = self.load_data(file_path)
        self.filename = file_path

    def process_image(self, size: float = 1) -> (np.array, int):
        """
        Load and prepare image data.
        :param size: image resizing factor
        :return
        """
        # Pad data array with zeros to make the shape isometric
        maximum = np.max(self.data.shape)
        out_img = np.zeros([maximum] * 3)

        a, b, c = self.data.shape
        x, y, z = (list(self.data.shape) - maximum) / -2

        out_img[int(x):a + int(x),
        int(y):b + int(y),
        int(z):c + int(z)] = self.data
        out_img /= out_img.max()  # all values should be <= 1

        # Resize image by the following factor
        if size != 1:
            out_img = resize(out_img, [int(size * maximum)] * 3)

        maximum = int(maximum * size)

        return out_img, maximum

    def generate_gif(self, size=1, frames_per_second: int = 18, colormap=None) -> None:
        """
        Creates and saves a NifTi image mosaic gif.
        :param size: size of the gif, between 0 and 1
        :param frames_per_second:
        :param colormap: cmaps are taken from matplotlib
        """
        out_img, maximum = self.process_image(size)
        new_img = self.create_standard_mosaic(out_img, maximum)

        if colormap is not None:
            # Transform values according to the color map
            cmap = get_cmap(colormap)
            color_transformed = [cmap(new_img[i, ...]) for i in range(maximum)]
            cmap_img = np.delete(color_transformed, 3, 3)
            new_img = cmap_img
        else:
            colormap = 'grayscale'

        self.save_gif(
            self.filename.replace(os.path.splitext(self.filename)[1], '_%s.gif' % colormap),
            new_img,
            frames_per_second,
            size
        )

    @staticmethod
    def create_standard_mosaic(out_img: np.array, maximum: int) -> np.array:
        """
        Creates grayscale image.
        """
        print('out image', out_img.shape)
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
        print('new img', new_img.shape)
        return new_img

    @staticmethod
    def load_data(filename: str) -> np.array:
        data = nb.load(filename).get_data()
        print('loaded data shape', data.shape)
        return data

    @staticmethod
    def save_gif(filename: str, gif_array: np.array, frames_per_second: int, resize_factor: float) -> None:
        mimwrite(
            filename,
            gif_array,
            format='gif',
            fps=int(frames_per_second * resize_factor)
        )
        print("Gif saved in %s" % filename)


if __name__ == "__main__":
    gif_generator = NiftyGifGenerator(
        file_path='/Users/etc.nii'
    )
    gif_generator.generate_gif()
    gif_generator.generate_gif(colormap='plasma')
    gif_generator.generate_gif(size=0.5, colormap='cubehelix')
    gif_generator.generate_gif(size=0.5, colormap='inferno')
    gif_generator.generate_gif(size=0.5, colormap='viridis')
