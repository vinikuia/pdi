import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib import pyplot as plt
import floodFillTrabalho4
import rotulaTrabalho4
import dados_de_rosto

INPUT_IMAGE = '2.bmp'
IS_CINZA = False # se True abre a imagem como GrayScale, se não abre como Colorida

TAMANHO_JANELA_ALTURA = 11
TAMANHO_JANELA_LARGURA = 15

def exec():
    dados_de_rosto.captura_dados_face()
