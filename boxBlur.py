import cv2 as cv
import numpy as np

FATOR_DE_CORRECAO_BETA = 0.3
FATOR_DE_CORRECAO_ALFA = 0.8
def execBoxBlur(img):
    img_cpy = np.copy(img)
    hsl_img = cv.cvtColor(img_cpy, cv.COLOR_RGB2HLS_FULL)

    shape_image = hsl_img.shape
    # th1 = cv.threshold(img_cpy, 180, 255, cv.THRESH_BINARY)
    lchannel = hsl_img[:, :, 1]
    mask = cv.inRange(lchannel, 0.6, 1)
    res = cv.bitwise_and(img_cpy, img_cpy, mask=mask)
    sum_blur = res
    for i in range(1,5,1):
        blur = cv.blur(res,(5*i,5*i),cv.BORDER_DEFAULT)
        sum_blur += blur


    hsl_img_cpy = hsl_img + sum_blur
    for i in range(0, shape_image[0]):
        for j in range(0, shape_image[1]):
            if hsl_img_cpy[i, j, 1] > 1:
                hsl_img_cpy[i, j, 1] = 1
    rgb_img_from_hsl = cv.cvtColor(hsl_img_cpy, cv.COLOR_HLS2RGB_FULL)
    return (img_cpy * FATOR_DE_CORRECAO_ALFA) + (FATOR_DE_CORRECAO_BETA*rgb_img_from_hsl)

    # cv.imshow('img_out', res)
    # cv.imshow('first_blur', res)
