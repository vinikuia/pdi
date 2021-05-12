import cv2
import numpy as np
import os

from pathlib import Path
import pickle

def face_recognition_trainer():
    dataset_path = "./dados_de_rosto/"
    if not os.path.exists(dataset_path):
        raise Exception('Não há rostos cadastrados no sistema até então')
    caminhos = [os.path.join(dataset_path, nome) for nome in os.listdir(dataset_path)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]

    faces = []

    for arq in arquivos:
        faces.append(np.load(arq))

    categories = [arquivos.index(f) for f in arquivos]
    names = [Path(f).stem for f in arquivos]
    labels = [None] * len(categories)
    for arq in arquivos:
        labels[arquivos.index(arq)] = Path(arq).stem
    with open("labels.pickle","wb") as f:
        pickle.dump(labels,f)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces,np.array(categories))
    recognizer.save("trainner.yml")


def face_recognition():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainner.yml")
    labels = {}
    with open("labels.pickle","rb") as f:
        labels = pickle.load(f)
    cascata_de_rosto = cv2.CascadeClassifier(cv2.haarcascades + "haarcascade_frontalface_alt.xml")
    skip = 0
    dados_de_rosto = []
    dataset_path = "./dados_de_rosto/"


    while True:
        ret, frame = cap.read()

        frame_escala_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if ret == False:
            continue
        rostos = cascata_de_rosto.detectMultiScale(frame_escala_cinza, 1.3, 5)
        k = 1
        rostos = sorted(rostos, key=lambda x: x[2] * x[3], reverse=True)
        skip += 1
        for rosto in rostos:
            x, y, w, h = rosto

            offset = 5
            rosto_offset = frame_escala_cinza[y - offset:y + h + offset, x - offset:x + w + offset]
            roi_gray = frame_escala_cinza[y - offset:y + h + offset]
            id_,conf = recognizer.predict(roi_gray)
            # print(conf) 
            if conf >= 0 and conf <=100:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255,255,255)
                stroke = 2
                cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)
            try:
                selecao_de_rosto = cv2.resize(rosto_offset, (100, 100))
            except Exception as e:
                # ignora imagens nas quais algum rosto esteja próximo a bora
                print(str(e))

            frameShape = frame.shape
            mask = np.zeros((frameShape[0], frameShape[1], 3), dtype=np.uint8)
            for i in range(y, y + h):
                for j in range(x, x + w):
                    mask[i][j][:] = 255
            cv2.imshow('mask', mask)
            blurredImage = cv2.GaussianBlur(frame, (35, 35), 0)
            blurredFace = np.where(mask == np.array([255, 255, 255]), blurredImage, frame)

            cv2.imshow(str(k), selecao_de_rosto)
            k += 1

            cv2.imshow("rostos_borrados", blurredFace)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("rostos", frame)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == ord('q'):
            break
