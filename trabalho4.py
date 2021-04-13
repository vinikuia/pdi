import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
import floodFillTrabalho4
import rotulaTrabalho4

#'60.bmp'
#'82.bmp'
#'114.bmp'
#'150.bmp'
#'205.bmp'

INPUT_IMAGE = '114.bmp'
IS_CINZA = True # se True abre a imagem como GrayScale, se não abre como Colorida

TAMANHO_JANELA_ALTURA = 11
TAMANHO_JANELA_LARGURA = 15

def exec():
    if IS_CINZA:
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()
    titles = ['image','mask','dilation','erosion','opening','closing','mg','th','img_tentativa']

    mask = cv2.medianBlur(img, 7) #borrando a imagem para lidar um pouco com o ruído inicial, usando blur da mediana por ser mais efetivo contra ruídos
    mask = cv2.adaptiveThreshold(mask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,7,2) #limiarizando a imagem com o gaussian blur (melhor para ruídos)
    cv2.floodFill(mask, None, (0,0), 0) #preencho o background de preto (já que nenhuma imagem tem um grão de arroz encostado na borda é só setar o flood fill no pixel 0,0
    kernal = np.ones((3,3),np.uint8) #kernel para morfologia
    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernal, iterations=2) #basta um opening (que nada mais é do que erodir -> dilatar em sequência, isso lida com os ruídos brancos
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernal, iterations=1)


    #cv2.imshow('binarizada-arroz-closing', closing)
    #cv2.imshow('binarizada-arroz-opening', opening)
    #cv2.imwrite('binarizada-arroz.bmp', mask)


    img_out = closing.astype(np.float32) / 255
    img_out = np.where(img_out == 1, -1, 0).astype(np.float32)


    componentes = rotulaTrabalho4.rotula(img_out)
    vetorAreas = []

    for items in componentes:
        vetorAreas.append(items['n_pixels'])

    vetorAreas = sorted(vetorAreas)
    vetorAreas = np.array(vetorAreas)

    cv2.imshow('img_out', img_out)

    areaLimiar = np.median(vetorAreas)

    riceCount = []

    for items in range (0,len(vetorAreas)):
        temp = vetorAreas[items]
        if areaLimiar * 1.9 < temp:
            riceCount.append(int(np.ceil(temp/areaLimiar)))
        else:
            riceCount.append(1)

    riceSum = 0
    for items in riceCount:
        riceSum += items

    print(riceSum)

    #images = [img,mask,opening,closing,mg,th,img_tentativa]
    # img_binarizada =cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    # cv2.imshow('img_binarizada',img_binarizada)
    for i in range(9):
        #plt.subplot(5, 2, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])

    #plt.show()
    cv2.waitKey() & 0xff
    cv2.destroyAllWindows()