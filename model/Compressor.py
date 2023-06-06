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
        if self.d < 0 or self.d > 2 * self.f - 2:
            raise Exception("Parametro d non valido")
        if self.f > self.img.shape[0] or self.f > self.img.shape[1]:
            raise Exception("Parametro F non valido")
        if len(self.img.shape) == 2:
            return self.compressGray()
        else:
            r = self.img[:, :, 0]
            g = self.img[:, :, 1]
            b = self.img[:, :, 2]
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
        self.removePixels()
        img_size = self.img.shape
        result = np.zeros(img_size)

        for i in r_[:img_size[0]:self.f]:
            for j in r_[:img_size[1]:self.f]:
                result[i:(i + self.f), j:(j + self.f)] = self.dct2(self.img[i:(i + self.f), j:(j + self.f)])
                result[i:(i + self.f), j:(j + self.f)] = self.deleteFrequencies(result[i:(i + self.f), j:(j + self.f)])
                result[i:(i + self.f), j:(j + self.f)] = self.idct2(result[i:(i + self.f), j:(j + self.f)])
                result[i:(i + self.f), j:(j + self.f)] = self.fixValues(result[i:(i + self.f), j:(j + self.f)])

        result = result.astype(int)
        return result

    def removePixels(self):
        height, width = self.img.shape

        rows_deleted = height % self.f
        columns_deleted = width % self.f

        if rows_deleted > 0:
            self.img = self.img[:-rows_deleted]
        if columns_deleted > 0:
            self.img = self.img[:, :-columns_deleted]

    @staticmethod
    def dct2(a):
        return dct(dct(a, axis=0, norm='ortho'), axis=1, norm='ortho')

    @staticmethod
    def idct2(a):
        return idct(idct(a, axis=0, norm='ortho'), axis=1, norm='ortho')

    def deleteFrequencies2(self, block):
        block[:, self.d:self.f] = 0
        for i in range(self.d):
            block[self.d - i:self.f, i] = 0
        return block

    def deleteFrequencies(self, block):
        v = np.arange(self.f)
        v = v.reshape(self.f, 1)
        a = np.zeros((self.f, self.f))
        a = a + v
        a = a + a.T
        block[a >= self.d] = 0
        return block

    @staticmethod
    def fixValues(block):
        block = np.round(block)
        block[block > 254] = 255
        block[block < 1] = 0
        return block