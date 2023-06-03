#! bin/python3
from model.Compressor import Compressor
from utilities.ImageReader import ImageReader
import matplotlib.pyplot as plt


def main():
    img = ImageReader.read_image('./img/bridge.bmp')
    # print(img.shape)
    f = 500
    d = 25
    c = Compressor(img, f, d)
    compressed = c.compress()
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
