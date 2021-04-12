import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

INPUT_IMAGE = '150.bmp'
IS_CINZA = True # se True abre a imagem como GrayScale, se não abre como Colorida

TAMANHO_JANELA_ALTURA = 11
TAMANHO_JANELA_LARGURA = 15

def exec():
    if IS_CINZA:
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()
    titles = ['image','mask','dilation','erosion','opening','closing','mg','th','img_tentativa']

    mask = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    kernal = np.ones((2,2),np.uint8)
    dilation =  cv2.dilate(mask,kernal,iterations=2)
    erosion = cv2.erode(mask,kernal,iterations=1)
    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernal)
    closing = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernal,iterations=4)
    mg = cv2.morphologyEx(mask,cv2.MORPH_GRADIENT,kernal)
    th = cv2.morphologyEx(mask,cv2.MORPH_TOPHAT,kernal)
    img_tentativa = cv2.morphologyEx(mg,cv2.MORPH_CLOSE,kernal,iterations=4)

    images = [img,mask,dilation,erosion,opening,closing,mg,th,img_tentativa]
    # img_binarizada =cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    # cv2.imshow('img_binarizada',img_binarizada)
    for i in range(9):
        plt.subplot(5, 2, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])

    plt.show()
    cv2.waitKey() & 0xff
    cv2.destroyAllWindows()