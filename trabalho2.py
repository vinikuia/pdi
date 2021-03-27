import sys
import cv2
import numpy as np
import filtroMediaIngenuo as fmi
import filtroMediaSeparavel as fms
import filtroMediaIntegrais as fmIntegrais
INPUT_IMAGE = 'a01 - Original.bmp'
IS_CINZA = True # se True abre a imagem como GrayScale, se não abre como Colorida

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
    imgFinalIngenua = fmi.executarFiltroMediaIngenuo(img, TAMANHO_JANELA_ALTURA, TAMANHO_JANELA_LARGURA)
    imgFinalSeparavel = fms.executarFiltroMediaSeparavel(img, TAMANHO_JANELA_ALTURA, TAMANHO_JANELA_LARGURA)
    imgFinalIntegral = fmIntegrais.executarFiltroMediaIntegrais(img, TAMANHO_JANELA_ALTURA, TAMANHO_JANELA_LARGURA)
    # Mantém uma cópia colorida para desenhar a saída.
    cv2.imshow('imgFiltroIngenuo', imgFinalIngenua)
    cv2.imwrite('imgFiltroIngenuo.png', imgFinalIngenua * 255)
    cv2.imshow('imgFinalSeparavel', imgFinalSeparavel)
    cv2.imwrite('imgFinalSeparavel.png', imgFinalSeparavel * 255)
    cv2.imshow('imgFinalIntegral', imgFinalIntegral)
    cv2.imwrite('imgFinalIntegral.png', imgFinalIntegral * 255)

    cv2.imshow('original', img)
    # cv2.imshow('02 - out', img_final)
    # cv2.imwrite('02 - out.png', img_final * 255)
    cv2.waitKey() & 0xff
    cv2.destroyAllWindows()