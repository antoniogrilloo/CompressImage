#! bin/python3
from numpy import r_
from scipy.fftpack import dct, idct
import numpy as np


class Compressor:

    def __init__(self, img, f, d):
        self.img = img
        self.f = f
        self.d = d

    def compress(self):
        if len(self.img.shape) == 2:
            return self.compressGray()
        r = self.img[:, :, 0]
        g = self.img[:, :, 1]
        b = self.img[:, :, 2]
        if self.d <= self.f:
            tmp = self.img
            self.img = r
            r = self.compressGray()
            self.img = g
            g = self.compressGray()
            self.img = b
            b = self.compressGray()
            self.img = tmp
        return np.stack((r, g, b), axis=2)

    def compressGray(self):
        rows_fill, columns_fill = self.fillDimensions()
        img_size = self.img.shape
        result = np.zeros(img_size)

        for i in r_[:img_size[0]:self.f]:
            for j in r_[:img_size[1]:self.f]:
                result[i:(i + self.f), j:(j + self.f)] = self.dct2(self.img[i:(i + self.f), j:(j + self.f)])
                result[i:(i + self.f), j:(j + self.f)] = self.deleteFrequencies(result[i:(i + self.f), j:(j + self.f)])
                result[i:(i + self.f), j:(j + self.f)] = self.idct2(result[i:(i + self.f), j:(j + self.f)])
                result[i:(i + self.f), j:(j + self.f)] = self.fixValues(result[i:(i + self.f), j:(j + self.f)])

        result = self.removeFilledPixels(result.astype(int), rows_fill, columns_fill)
        return result

    def fillDimensions(self):
        rows_to_fill = 0
        col_to_fill = 0
        height, width = self.img.shape

        if height % self.f > 0:
            rows_to_fill = self.f - height % self.f
            last_pixels = self.img[-rows_to_fill:]
            self.img = np.r_[self.img, last_pixels]

        if width % self.f > 0:
            col_to_fill = self.f - width % self.f
            last_pixels = self.img[:, width - col_to_fill:width]
            self.img = np.c_[self.img, last_pixels]

        return rows_to_fill, col_to_fill

    @staticmethod
    def dct2(a):
        return dct(dct(a, axis=0, norm='ortho'), axis=1, norm='ortho')

    @staticmethod
    def idct2(a):
        return idct(idct(a, axis=0, norm='ortho'), axis=1, norm='ortho')

    def deleteFrequencies(self, block):
        block[:, self.d:self.f] = 0
        for i in range(self.d):
            block[self.d - i:self.f, i] = 0
        return block

    @staticmethod
    def fixValues(block):
        block = np.round(block)
        block[block > 254] = 255
        block[block < 1] = 0
        return block

    @staticmethod
    def removeFilledPixels(matrix, rows_fill, columns_fill):
        if rows_fill > 0:
            matrix = matrix[:-rows_fill]
        if columns_fill > 0:
            matrix = matrix[:, :-columns_fill]
        return matrix