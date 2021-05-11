import cv2
import numpy as np
import os

def captura_dados_face():

    cap= cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cascata_de_rosto = cv2.CascadeClassifier(cv2.haarcascades+ "haarcascade_frontalface_alt.xml")
    skip = 0
    dados_de_rosto = []
    dataset_path = "./dados_de_rosto/"

    nome_do_arquivo = input("Qual o nome desse rosto??")

    ret, frame = cap.read()
    frameShape = frame.shape
    maskRostos = np.zeros((frameShape[0], frameShape[1], 3), dtype=np.uint8)


    while True:
        ret,frame = cap.read()
        mask = np.zeros((frameShape[0], frameShape[1], 3), dtype=np.uint8)
        frame_escala_cinza = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if ret == False:
            continue
        rostos = cascata_de_rosto.detectMultiScale(frame_escala_cinza,1.3,5)
        k=1
        rostos = sorted(rostos,key =lambda x : x[2]*x[3], reverse=True)
        skip +=1
        for rosto in rostos[:1]:
            x,y,w,h = rosto

            offset = 5
            rosto_offset = frame[y-offset:y+h+offset,x-offset:x+w+offset]
            try:
                selecao_de_rosto = cv2.resize(rosto_offset,(100,100))
            except Exception as e:
                # ignora imagens nas quais algum rosto esteja próximo a bora
                print(str(e))
            if skip % 10 == 0:
                dados_de_rosto.append(selecao_de_rosto)
                print(len(dados_de_rosto))



            for i in range (y, y + h):
                for j in range (x, x+w):
                    mask[i][j][:] = 255

            maskRostos += mask

            # for i in range (0, frameShape[0]):
            #     for j in range (0, frameShape[1]):
            #         if maskRostos[i][j].any() > 255:
            #             maskRostos[i][j][:] = 255


            cv2.imshow('mask', maskRostos)
            blurredImage = cv2.GaussianBlur(frame, (35,35), 0)
            blurredFace = np.where(maskRostos >= np.array([255, 255, 255]), blurredImage, frame)
            cv2.imshow("rostos_borrados", blurredFace)
            cv2.imshow(str(k),selecao_de_rosto)
            k+=1


            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
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