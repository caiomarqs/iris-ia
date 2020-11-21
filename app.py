from flask import Flask, render_template, Response
import face_recognition
import cv2 
import numpy as np
from io import BytesIO
from pesquisaBD import users_analyse 
from pesquisaBD import users_directories 
import utils
import os
from os import listdir

#Initializa o app Flask 
app = Flask(__name__)

# Obtem uma referência para a webcam 
video_capture = cv2.VideoCapture(0)

# Criando lista de rostos conhecidos  
known_face_encodings = []

# Convertendo a lista de string para int
users_directories = list(map(int, users_directories))

# Carregando imagem do cliente e aprendendo reconhecê-lo
for i in range(len(users_directories)):
    basedir = 'Images/' + str(users_directories[i]) 
    diretorio = listdir(basedir)
    base64img = open(basedir + '/' + diretorio[0]).read()
    image = utils.string_to_image(base64img)

    cliente_image = face_recognition.load_image_file(image)
    known_face_encodings.append(face_recognition.face_encodings(cliente_image)[0])
    users_directories[i] = users_directories[i] + 1

# Initializando variáveis
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def gen_frames():
    process_this_frame = True
    while True:
        # Pega um único quadro do video
        ret, frame = video_capture.read()

        # Redimensiona o quadro para 1/4 para um processamento mais rápido
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Converte a imagem de BGR (do OpenCV) para cor RGB (usada pelo face_recognition)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Processa quadros alternados para economizar tempo 
        if process_this_frame:
            # Encontra todos os rostos no quadro
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # Comparando o rosto com os rostos conhecidos
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Desconhecido"

                # Usando o rosto conehcido que tem a menor distância para o novo
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = users_analyse[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Exibe o resultado
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Dimensiona os locais dos rostos
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Desenha uma caixa ao redor do rosto
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Coloca o nome do cliente reconhecido
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()