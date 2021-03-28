import cv2 as cv
import numpy as np

def execGaussianBloom(img):
    img_cpy = np.copy(img)
    hsl_img = cv.cvtColor(img_cpy, cv.COLOR_RGB2HLS_FULL)

    shape_image = hsl_img.shape
    # th1 = cv.threshold(img_cpy, 180, 255, cv.THRESH_BINARY)
    lchannel = hsl_img[:, :, 1]
    mask = cv.inRange(lchannel, 0.6, 1)
    res = cv.bitwise_and(img_cpy, img_cpy, mask=mask)
    sum_blur = res
    for i in range(1,9,2):
        blur = cv.GaussianBlur(res,(5*i,5*i),cv.BORDER_DEFAULT)
        cv.imshow(str(i)+'_blur', sum_blur)
        sum_blur += blur

    for i in range(0, shape_image[0]):
        for j in range(0, shape_image[1]):
            if sum_blur[i, j, 1] > 1:
                sum_blur[i, j, 1] = 1

    hsl_img_cpy = hsl_img + sum_blur
    rgb_img_from_hsl = cv.cvtColor(hsl_img, cv.COLOR_HLS2RGB_FULL)
    cv.imshow('hsl_img_cpy', hsl_img_cpy)
    cv.imshow('rgb_img_from_hsl_final', img_cpy + (0.8*rgb_img_from_hsl))

    # cv.imshow('img_out', res)
    # cv.imshow('first_blur', res)




