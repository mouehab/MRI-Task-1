import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import sys

path = sys.argv[1]
if os.path.exists(path):
    print(os.path.basename(path))
    img = cv2.imread(path,0)
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))

    plt.subplot(121),plt.imshow(img, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Fourier Spectrum'), plt.xticks([]), plt.yticks([])
    plt.show()