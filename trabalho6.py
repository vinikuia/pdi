import dados_de_rosto
import face_recognition

INPUT_IMAGE = '2.bmp'
IS_CINZA = False # se True abre a imagem como GrayScale, se não abre como Colorida

TAMANHO_JANELA_ALTURA = 11
TAMANHO_JANELA_LARGURA = 15

def exec():
    dados_de_rosto.captura_dados_face()
    face_recognition.face_recognition_trainer()
    face_recognition.face_recognition()