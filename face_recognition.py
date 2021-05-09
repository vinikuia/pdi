import cv2
import numpy as np
import os

def distance(v1,v2):
    # distancia euclidiana
    return np.sqrt(((v1-v2)**2).sum())

def knn(train,test,k=5):
    dist = []

    for i in range(train.shape):
        #captura o vetor e nomeia
        ix = train[i, :-1]
        iy = train[i,-1]

        d = distance(test,ix)
        dist.append([d,iy])
    dk = sorted(dist,key=lambda x: x[0])[:k]

    rotulos = np.array(dk)[:,-1]
    output = np.unique(rotulos,return_counts=True)

    index = np.argmax(output[1])
    return output[0][index]

def face_recognition():
    cap = cv2.VideoCapture(0)
    cascata_de_rosto = cv2.CascadeClassifier(cv2.haarcascades+ "haarcascade_frontalface_alt.xml")
    dados_de_rosto = []
    dataset_path = "./dados_de_rosto"
    rotulos =[]
    class_id = 0
    nomes = {}
    known_face_encodings = [
        obama_face_encoding,
        biden_face_encoding
    ]
    known_face_names = [
        "Barack Obama",
        "Joe Biden"
    ]
    while True:
        # Grab a single frame of video
        ret, frame = cap.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)