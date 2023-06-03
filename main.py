#! bin/python3
import time

from model.Compressor import Compressor
from utilities.ImageReader import ImageReader
import matplotlib.pyplot as plt


def main():
    img = ImageReader.read_image('./img/deer.bmp')
    print(img.shape)
    f = 500
    d = 100
    c = Compressor(img, f, d)
    t0 = time.time()
    compressed = c.compress()
    t1 = time.time()
    print("TEMPO COMPRESSIONE: " + str(t1 - t0))
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(img, cmap=plt.get_cmap('gray'), vmin=0, vmax=255)
    ax1.set_title('Original')
    ax2.imshow(compressed, cmap=plt.get_cmap('gray'), vmin=0, vmax=255)
    ax2.set_title('Compressed')
    ax1.axis('off')
    ax2.axis('off')
    plt.show()


if __name__ == '__main__':
    main()
