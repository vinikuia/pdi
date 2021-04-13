def floodFillRecursivo(img, i, j, rotulo):
    if img[i][j] != -1.0:
        return 0
    if img[i][j] != -1.0:
        return 0
    coordenadas = [(i, j)]
    tam = 1
    shape = img.shape
    img[i][j] = rotulo
    if shape[0] <= i+1 and shape[1] <= j+1 and i-1 >=0 and j-1 >=0:
        if  img[i+1][j] == -1.0:
            aux = floodFillRecursivo(img, i + 1, j, rotulo)
            for item in aux:
                coordenadas.append(item)
        if img[i-1][j] == -1.0:
            aux = floodFillRecursivo(img, i - 1, j, rotulo)
            for item in aux:
                coordenadas.append(item)
        if img[i][j+1] == -1.0:
            aux = floodFillRecursivo(img, i, j + 1, rotulo)
            for item in aux:
                coordenadas.append(item)
        if img[i][j-1] == -1.0:
            aux = floodFillRecursivo(img, i, j - 1, rotulo)
            for item in aux:
                coordenadas.append(item)
    return coordenadas[0:coordenadas.__sizeof__()]
