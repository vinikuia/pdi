import sys
import timeit
import numpy as np
import cv2
import binariza
import rotula

INPUT_IMAGE = 'arroz.bmp'

NEGATIVO = False
THRESHOLD = 0.8


def trabalhoArroz():
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype(np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza.binariza(img, THRESHOLD)
    cv2.imshow('01 - binarizada',  img*(-255))
    cv2.imwrite('01 - binarizada.png', img*(-255))

    start_time = timeit.default_timer()
    componentes = rotula.rotula(img)
    n_componentes = len(componentes)
    print('Tempo: %f' % (timeit.default_timer() - start_time))
    print('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle(img_out, (c['L'], c['T']), (c['R'], c['B']), (0, 0, 1))

    cv2.imshow('02 - out', img_out)
    cv2.imwrite('02 - out.png', img_out * 255)
    cv2.waitKey() & 0xff
    cv2.destroyAllWindows()