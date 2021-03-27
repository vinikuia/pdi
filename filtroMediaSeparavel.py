from math import floor
import cv2

import numpy as np

def executarFiltroMediaSeparavel(img,altura,largura):
    img_cpy = np.copy(img)
    shape_img = img.shape
    return filtroMediaSeparavel(img, img_cpy, shape_img,altura,largura)

def filtroMediaSeparavel(img, img_cpy, shape_img,altura,largura):

    for i in range(0, shape_img[0]):
        for j in range(0, shape_img[1]):
            for camada in range(0, shape_img[2]):
                soma = 0
                contador=0
                for l in range((j - floor(altura / 2)), j + floor(largura / 2)):
                    if l >0 and l <shape_img[1]:
                        contador+=1
                        soma += img[i][l][camada]
                valorPixel = float(soma / contador)
                img_cpy[i][j][camada] = valorPixel

    img_cpy_final = np.copy(img_cpy)

    for i in range(0, shape_img[0]):
        for j in range(0, shape_img[1]):
            for camada in range(0, shape_img[2]):
                soma = 0
                contador = 0
                for k in range((i - floor(altura / 2)), i + floor(largura / 2)):
                    if k > 0 and k < shape_img[0]:
                        contador += 1
                        soma += img_cpy[k][j][camada]
                valorPixel = float(soma / contador)
                img_cpy_final[i][j][camada] = valorPixel
    return img_cpy_final
