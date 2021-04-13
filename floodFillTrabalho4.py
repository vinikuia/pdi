def floodFillRecursivo(img, i, j,shape, rotulo):
    if img[i][j] != -1.0:
        return 0
    if img[i][j] != -1.0:
        return 0
    coordenadas = [(i, j)]
    tam = 1
    img[i][j] = rotulo
    # shape[0] <= i + 1 and shape[1] <= j + 1 and i - 1 >= 0 and j - 1 >= 0:
    if img[i+1][j] == -1.0:
        aux = floodFillRecursivo(img, i + 1, j,shape, rotulo)
        for item in aux:
            coordenadas.append(item)
    if img[i-1][j] == -1.0:
        aux = floodFillRecursivo(img, i - 1, j,shape, rotulo)

        for item in aux:
            coordenadas.append(item)
    if img[i][j+1] == -1.0:
        aux = floodFillRecursivo(img, i, j + 1,shape, rotulo)
        for item in aux:
            coordenadas.append(item)
    if img[i][j-1] == -1.0:
        aux = floodFillRecursivo(img, i, j - 1, shape,rotulo)
        for item in aux:
            coordenadas.append(item)
    if not isinstance(coordenadas[0:coordenadas.__sizeof__()],list):
        print(coordenadas[0:coordenadas.__sizeof__()])
    return coordenadas[0:coordenadas.__sizeof__()]
