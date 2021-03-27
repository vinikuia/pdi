from math import floor
import cv2

import numpy as np

def executarFiltroMediaIntegrais(img,altura,largura):
    img_cpy = np.copy(img)
    shape_img = img.shape
    return filtroMediaIntegrais(img, img_cpy, shape_img,altura,largura)

def filtroMediaIntegrais(img, img_cpy, shape_img,altura,largura):
    for i in range(0, shape_img[0]):
        soma = [0,0,0]
        for j in range(0, shape_img[1]):
            for camada in range(0, shape_img[2]):
                soma[camada] += img[i][j][camada]
                img_cpy[i][j][camada] = soma[camada]
    for j in range(0, shape_img[1]):
        soma = [0,0,0]
        for i in range(0, shape_img[0]):
            for camada in range(0, shape_img[2]):
                soma[camada] += img_cpy[i][j][camada]
                img_cpy[i][j][camada] += soma[camada]
                img_cpy[i][j][camada] -= img[i][j][camada]
    img_cpy_final = np.copy(img_cpy)
    for i in range(0, shape_img[0]):
        for j in range(0, shape_img[1]):
            for camada in range(0, shape_img[2]):
                coluna = j - largura if j - largura > 0 else 0
                linha = i - altura if i - altura > 0 else 0
                rb = img_cpy[i][j][camada]
                rt = img_cpy[linha][j][camada]
                lt = img_cpy[linha][coluna][camada]
                lb = img_cpy[i][coluna][camada]
                tamanhoAltura = altura
                tamanhoLargura = largura
                if(i < altura):
                    tamanhoAltura = i if i != 0 else 1
                if(j < largura):
                    tamanhoLargura = j if j != 0 else 1
                tamanhoJanela = tamanhoAltura * tamanhoLargura
                if i == 0 and j == 0:
                    soma = rb
                elif i == 0 or j == 0:
                    soma = rb - lt
                else:
                    soma = rb - rt - lb + lt
                valorPixel = float(soma / tamanhoJanela)
                img_cpy_final[i][j][camada] = valorPixel
    return img_cpy_final
