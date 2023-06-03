#! /usr/bin/python3

import numpy as np
from numpy import float64
from scipy.fftpack import dct, idct
import time
import matplotlib.pyplot as plt


def gen_and_save_matrices(number, save):
    ms = []
    dim = 60
    for i in range(number):
        n = dim * 2 ** i
        m = np.round(np.random.rand(n, n) * 255)
        ms.append(m)
        if save:
            filename = './test_matrices/m' + str(n) + '.npy'
            np.save(filename, m)
    return ms


# Returns a vector of matrices
def load_matrices_from_file(n):
    m = []
    numbers = n * 2 + 2
    for i in range(2, numbers, 2):
        filename = './test_matrices/m' + str(i) + '.npy'
        m.append(np.load(filename))
    return m


# Returns times in order by matrix size (2, 4, 6, ...)
def measure_time(m, fun):
    l = len(m)
    times = np.zeros(l)
    for i in range(l):
        mt = m[i]
        t0 = time.time()
        fun(mt)
        t1 = time.time()
        times[i] = t1 - t0
    return times


def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')


def test_dct():
    mat = np.array([[231, 32, 233, 161, 24, 71, 140, 245],
                    [247, 40, 248, 245, 124, 204, 36, 107],
                    [234, 202, 245, 167, 9, 217, 239, 173],
                    [193, 190, 100, 167, 43, 180, 8, 70],
                    [11, 24, 210, 177, 81, 243, 8, 112],
                    [97, 195, 203, 47, 125, 114, 165, 181],
                    [193, 70, 174, 167, 41, 30, 127, 245],
                    [87, 149, 57, 192, 65, 129, 178, 228]])
    res = dct2(mat)
    print("DCT LIBRERIA: ")
    for i in range(8):
        for j in range(8):
            print('%.2e' % res[i, j], end='\t')
        print()
    print()
    res = dct(mat[0, :], norm="ortho")
    for i in range(8):
        print('%.2e ' % res[i], end='\t')
    print()
    res = my_dct2(mat)
    print("\nMY DCT:")
    for i in range(8):
        for j in range(8):
            print('%.2e' % res[i, j], end='\t')
        print()
    print()
    res = my_dct(mat[0, :])
    for i in range(8):
        print('%.2e ' % res[i], end='\t')


def my_dct(v):
    n = len(v)
    a = np.zeros(n)
    w = np.arange(n)
    w[w != 0] = n / 2
    w[w == 0] = n
    w = np.sqrt(w)
    i = np.arange(n)
    for k in range(n):
        a[k] = (v * np.cos(np.pi * k * ((2 * i + 1) / (2 * n)))).sum()
    a = a / w
    return a


def my_dct2(mat):
    n, m = np.shape(mat)
    res = np.array(mat, dtype=float64)
    for i in range(n):
        res[i] = my_dct(res[i])
    for j in range(m):
        res[:, j] = my_dct(res[:, j])
    return res


def main():
    plt.rcParams["text.usetex"] = True
    n = 7
    m = gen_and_save_matrices(n, False)
    # m = load_matrices_from_file(n)
    times_my_dct = np.log10(measure_time(m, my_dct2))
    times_dct = np.log10(measure_time(m, dct2))
    pix_start = 60
    numbers = np.array([pix_start * 2 ** i for i in range(n)])

    x3 = np.log10(numbers ** 3)
    x2logx = np.log10(numbers ** 2 * np.log(numbers))

    # for legend
    color = ['red', 'green', 'blue', 'gold']
    names = [r'$x^3$', r'$x^2 log x$', r'DCT implementata', r'DCT libreria']

    plt.plot(numbers, x3, color=color[0], label=names[0])
    plt.plot(numbers, x2logx, color=color[1], label=names[1])
    plt.plot(numbers, times_my_dct, color=color[2], label=names[2])
    plt.plot(numbers, times_dct, color=color[3], label=names[3])
    plt.title("Confronti tra DCT2")
    plt.xlabel("Dimensione matrice")
    plt.ylabel("Tempo")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # test_dct()
    main()
