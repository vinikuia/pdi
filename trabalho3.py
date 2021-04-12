import sys
import cv2
import numpy as np
import gaussianBloom as gb
import boxBlur as bb

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
    imgFinalGaussiana = gb.execGaussianBloom(img)
    imgFinalBoxBlur = bb.execBoxBlur(img)

    cv2.imshow(INPUT_IMAGE + 'imgFinalGaussiana - out', imgFinalGaussiana)
    cv2.imwrite(INPUT_IMAGE+'imgFinalGaussiana - out.png', imgFinalGaussiana * 255)
    cv2.imshow(INPUT_IMAGE+'imgFinalBoxBlur - out', imgFinalBoxBlur)
    cv2.imwrite(INPUT_IMAGE+'imgFinalBoxBlur - out.png', imgFinalBoxBlur * 255)
    cv2.waitKey() & 0xff
    cv2.destroyAllWindows()