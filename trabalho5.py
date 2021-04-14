import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
import floodFillTrabalho4
import rotulaTrabalho4


INPUT_IMAGE = '0.bmp'
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

    background =cv2.imread("Wind Waker GC.bmp", cv2.IMREAD_COLOR)
    img = cv2.resize(img, (640, 480))
    background = cv2.resize(background, (640, 480))

    u_green = np.array([255, 86, 255])
    l_green = np.array([0, 36, 0])

    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV_FULL)
    mask = cv2.inRange(hsv_img, l_green, u_green)
    res = cv2.bitwise_and(hsv_img, hsv_img, mask=mask)


    hsv_img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB_FULL)

    f = hsv_img - res
    cv2.imshow("mask", f)
    f = np.where(f == 0, background, f)
    cv2.imshow("mask2", f)

    cv2.imshow("video", img)
    cv2.imshow("masked_image", hsv_img)
    # background =cv2.imread("Wind Waker GC.bmp", cv2.IMREAD_COLOR)
    # img = cv2.resize(img, (640, 480))
    # background = cv2.resize(background, (640, 480))
    #
    # image_copy = np.copy(img)
    # image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
    # lower_blue = np.array([0, 0, 100])  ##[R value, G value, B value]
    # upper_blue = np.array([120, 100, 255])
    # mask = cv2.inRange(image_copy, lower_blue, upper_blue)
    # masked_image = np.copy(image_copy)
    # res = cv2.bitwise_and(image_copy, image_copy, mask=mask)
    # cv2.imshow('mask',res)
    #
    # cv2.imshow('masked_image',masked_image)
    #
    # background[mask == 0] = [0, 0, 0]
    # final_image = background + masked_image
    # cv2.imshow('final',final_image)
    cv2.waitKey() & 0xff

    cv2.destroyAllWindows()