import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib import pyplot as plt
import floodFillTrabalho4
import rotulaTrabalho4


INPUT_IMAGE = '8.bmp'
IS_CINZA = False # se True abre a imagem como GrayScale, se não abre como Colorida

TAMANHO_JANELA_ALTURA = 11
TAMANHO_JANELA_LARGURA = 15

def exec():
    # COM RGB

    # if IS_CINZA:
    #     img = cv2.imread(INPUT_IMAGE,cv2.IMREAD_COLOR)
    # else:
    #     img = cv2.imread(INPUT_IMAGE,cv2.IMREAD_COLOR)
    # if img is None:
    #     print('Erro abrindo a imagem.\n')
    #     sys.exit()
    #
    # background = cv2.imread("Wind Waker GC.bmp",cv2.IMREAD_COLOR)
    # img = cv2.resize(img, (640, 480))
    # cv2.imshow('img',img)
    # background = cv2.resize(background, (640, 480))
    #
    # l_green = np.array([0, 140, 0])
    # u_green = np.array([150, 255, 150])
    # mask = cv2.inRange(img, l_green, u_green)
    # masked_image = np.copy(img)
    # masked_image[mask!=0] = [0,0,0],
    # cv2.imshow('masked_image',masked_image)
    # background_image = background.copy()
    # background_image[mask==0] = [0,0,0],
    # final_image = background_image + masked_image
    # cv2.imshow('final_image',final_image)


    # COM HSV

    img = cv2.imread(INPUT_IMAGE)
    img = cv2.resize(img,(640,480))

    shape_img = img.shape

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    background = cv2.imread("Wind Waker GC.bmp")
    background = cv2.cvtColor(background, cv2.COLOR_BGR2HSV)
    background = cv2.resize(background,(640,480))
    # define range of green color in HSV
    lower_green = np.array([36, 100, 100])
    upper_green = np.array([90, 255, 255])
    # Threshold the HSV image to extract green color
    mask = cv2.inRange(hsv_img, lower_green, upper_green)
    show_result('mask', mask, 0) #interesse = 255

    # R = 0
    # G = 0
    # B = 0
    # contador = 0
    #
    # for i in range (0, shape_img[0]):
    #     for j in range (0, shape_img[1]):
    #         if mask[i][j] == 255:
    #             R += img[i][j][0]
    #             G += img[i][j][1]
    #             B += img[i][j][2]
    #             contador += 1
    # R = R/contador
    # G = G/contador
    # B = B/contador
    # print(R,G,B)
    # lower_green = np.array([36, G-75, 100])
    # upper_green = np.array([90, G+75, 255])
    # mask = cv2.inRange(hsv_img, lower_green, upper_green)
    # show_result('mask', mask, 0)

    bordas = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    img_bordas = np.zeros((shape_img[0],shape_img[1],shape_img[2]), np.uint8)
    cv2.drawContours(img_bordas,bordas, -1, (255,255,255), 3)

    mask = cv2.bitwise_not(mask)
    # show_result('mask', mask, 0)
    masked_image = np.copy(hsv_img)
    masked_image[mask==0] = [0,0,0],
    # show_result('masked_image', masked_image, 0)
    background_image = background.copy()
    background_image[mask!=0] = [0,0,0]
    # show_result('background_image', background_image, 0)
    final_image = background_image + masked_image
    final_image= cv2.cvtColor(final_image, cv2.COLOR_HSV2BGR)
    blurred = cv2.GaussianBlur(final_image, (7,7), 0)
    blurred_final_image = np.where(bordas==np.array([255,255,255]), final_image, blurred)
    show_result('final_image', final_image, 0)
    show_result('blurred_img', blurred_final_image, 0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def show_result(winname, img, wait_time):
    scale = 0.2
    cv2.imshow(winname, img)
