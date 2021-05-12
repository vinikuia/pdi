import cv2
import numpy as np
import os

def captura_dados_face():

    cap= cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cascata_de_rosto = cv2.CascadeClassifier(cv2.haarcascades+ "haarcascade_frontalface_alt.xml")
    # cascata_de_olho = cv2.CascadeClassifier(cv2.haarcascades+ "haarcascade_eye.xml")
    # cascata_de_sorriso =  cv2.CascadeClassifier(cv2.haarcascades+ "haarcascade_smile.xml")
    skip = 0
    dados_de_rosto = []
    dataset_path = "./dados_de_rosto/"

    nome_do_arquivo = input("Qual o nome desse rosto??")

    while True:
        ret, frame = cap.read()
        if ret != False:
            frameShape = frame.shape
            mask = np.zeros((frameShape[0], frameShape[1], 3), dtype=np.uint8)

        frame_escala_cinza = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if ret == False:
            continue
        rostos = cascata_de_rosto.detectMultiScale(frame_escala_cinza,1.5,5)
        k=1
        rostos = sorted(rostos,key =lambda x : x[2]*x[3], reverse=True)
        skip +=1

        for rosto in rostos:
            x,y,w,h = rosto
            offset = 5
            rosto_offset = frame_escala_cinza[y-offset:y+h+offset,x-offset:x+w+offset]
            try:
                selecao_de_rosto = cv2.resize(rosto_offset,(100,100))
            except Exception as e:
                # ignora imagens nas quais algum rosto esteja próximo a bora
                print(str(e))
            if skip % 5 == 0:
                dados_de_rosto.append(rosto_offset)
                print(len(dados_de_rosto))

            for i in range (y, y + h):
                for j in range (x, x+w):
                    mask[i][j][:] = 255

            cv2.imshow('mask', mask)
            blurredImage = cv2.GaussianBlur(frame, (35, 35), 0)
            blurredFace = np.where(mask == np.array([255, 255, 255]), blurredImage, frame)
            cv2.imshow("rostos_borrados", blurredFace)


            cv2.imshow(str(k),selecao_de_rosto)
            k+=1


            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            # olhos = cascata_de_olho.detectMultiScale(frame_escala_cinza,1.5,5)
            # for olho in olhos:
            #     ox, oy, ow, oh = olho
            #     cv2.rectangle(frame, (ox, oy), (ox + ow, oy + oh), (0, 255, 0), 2)

            # sorrisos = cascata_de_sorriso.detectMultiScale(frame_escala_cinza,2,5)
            # for sorriso in sorrisos:
            #     sx, sy, sw, sh = sorriso
            #     cv2.rectangle(frame, (sx, sy), (sx + sw, sy + sh), (0, 255, 0), 2)

        cv2.imshow("rostos",frame)

        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == ord('q'):
            break
    dados_de_rosto = np.array(dados_de_rosto)
    dados_de_rosto = dados_de_rosto.reshape((dados_de_rosto.shape[0],-1))


    # construct the directory string

    # check the directory does not exist
    if not (os.path.exists(dataset_path)):
        # create the directory you want to save to
        os.mkdir(dataset_path)

        ds = {"ORE_MAX_GIORNATA": 5}

    np.save(dataset_path + nome_do_arquivo, dados_de_rosto)

    cap.release()
    cv2.destroyAllWindows()