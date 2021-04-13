import floodFillTrabalho4

ALTURA_MIN = 10
LARGURA_MIN = 10

def rotula(img):
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    # TODO: escreva esta função.
    # Use a abordagem com flood fill recursivo.
    rotulo = 0.0
    shape = img.shape
    arroz = 0
    lista = []

    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            if img[i][j] == -1.0:
                # print (i,j)
                # sys.exit()
                menor_linha = shape[0]
                maior_linha = 1
                menor_coluna = shape[1]
                maior_coluna = 1
                rotulo += 0.005
                tamanho = floodFillTrabalho4.floodFillRecursivo(img, i, j, shape,rotulo)
                # for item in tamanho:
                    # if item[0] < menor_linha:
                    #     menor_linha = item[0]
                    # if item[0] > maior_linha:
                    #     maior_linha = item[0]
                    # if item[1] < menor_coluna:
                    #     menor_coluna = item[1]
                    # if item[1] > maior_coluna:
                    #     maior_coluna = item[1]
                # lista.append({'label': rotulo, 'n_pixels': tamanho.__sizeof__(
                # ), 'T': menor_linha, 'L': menor_coluna, 'B': maior_linha, 'R': maior_coluna})
                lista.append({'n_pixels': tamanho.__sizeof__()})
    return lista
