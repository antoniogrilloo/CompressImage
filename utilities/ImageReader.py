#! bin/python3

import imageio.v3 as iio


class ImageReader:

    @staticmethod
    def read_image(filename):
        return iio.imread(filename)
