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

#multiplicador do tamanho da área do arroz mediano, quanto menor, menor o blob de arroz precisa ser para ser contado como mais do que um arroz.
#Valores entre 1 e 2 são ideais, menores que 1 multiplicariam arroz únicos e maiores que 2 contariam junções de arroz como únicos.
MULTIPLICADOR = 1.4

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

    mask = cv2.medianBlur(img, 7) #borrando a imagem para lidar um pouco com o ruído inicial, usando blur da mediana por ser mais efetivo contra ruídos
    mask = cv2.adaptiveThreshold(mask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,7,2) #limiarizando a imagem com o gaussian blur (melhor para ruídos)
    cv2.floodFill(mask, None, (0,0), 0) #preencho o background de preto (já que nenhuma imagem tem um grão de arroz encostado na borda é só setar o flood fill no pixel 0,0
    kernal = np.ones((3,3),np.uint8) #kernel para morfologia
    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernal, iterations=2) #basta um opening (que nada mais é do que erodir -> dilatar em sequência, isso lida com os ruídos brancos
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernal, iterations=1)

    img_out = closing.astype(np.float32) / 255
    img_out = np.where(img_out == 1, -1, 0).astype(np.float32)

    componentes = rotulaTrabalho4.rotula(img_out) #floodfill similar a versão do trabalho 1, retorna a área total do blob de interesse (contagem de pixeis)
    vetorAreas = []

    for items in componentes:
        vetorAreas.append(items['n_pixels']) #passamos esses valores da área dos blobs para um vetor

    vetorAreas = sorted(vetorAreas) #ordenamos o vetor
    vetorAreas = np.array(vetorAreas)

    areaLimiar = np.median(vetorAreas) #pegamos a área do arroz mediano (supõe-se que é um arroz único por conta da quantidade de arroz soltos e a baixa quantidade de ruído e blobs de arroz grudados)
                                       #caso existisse uma imagem com muitos blobs basta pegar um arroz mais no início do vetor, se fosse imagem com muitos ruídos, um arroz mas ao final do vetor.
    riceCount = []

    for items in range (0,len(vetorAreas)):  #inserimos em uma lista arroz por arroz,e caso o blob seja maior do que a área do arroz mediano, supõe-se que são vários grudados
        temp = vetorAreas[items]
        if areaLimiar * MULTIPLICADOR < temp: #caso sejam diversos arroz grudados, dividimos a área do blob pela área do arroz mediano
            riceCount.append(int(np.ceil(temp/areaLimiar)))
        elif areaLimiar * 0.3 > temp: #caso a área não seja muito pequena (em caso de ruído), não é arroz
            riceCount.append(0)
        else: #caso contrário é um único arroz
            riceCount.append(1)

    riceSum = 0
    for items in riceCount: #percorremos a lista riceCount somando todos os itens dela (número de arroz) para finalizar a contagem
        riceSum += items

    cv2.imshow('Rotulada-Arroz',img_out)
    cv2.imshow('Imagem-Original', img)
    cv2.imwrite('Rotulada-Arroz.bmp', img_out*255)

    print(riceSum)

    cv2.waitKey() & 0xff
    cv2.destroyAllWindows()