import sys
import cv2
import numpy as np
import gaussianBloom as gb

INPUT_IMAGE = 'Wind Waker GC.bmp'
IS_CINZA = False # se True abre a imagem como GrayScale, se não abre como Colorida

TAMANHO_JANELA_ALTURA = 11
TAMANHO_JANELA_LARGURA = 15

def exec():
    if IS_CINZA:
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()
    if IS_CINZA:
        img = img.reshape((img.shape[0], img.shape[1], 1))
    else:
        img = img.reshape((img.shape[0], img.shape[1], 3))

    img = img.astype(np.float32) / 255
    imgFinalIngenua = gb.execGaussianBloom(img)
    # cv2.imshow('02 - out', img_final)
    # cv2.imwrite('02 - out.png', img_final * 255)
    cv2.waitKey() & 0xff
    cv2.destroyAllWindows()