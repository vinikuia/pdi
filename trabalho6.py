import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib import pyplot as plt
import floodFillTrabalho4
import rotulaTrabalho4


INPUT_IMAGE = '2.bmp'
IS_CINZA = False # se True abre a imagem como GrayScale, se não abre como Colorida

TAMANHO_JANELA_ALTURA = 11
TAMANHO_JANELA_LARGURA = 15

def exec():
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame = cap.read()
        if ret == False:
            continue
        cv2.imshow('video frame',frame)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
