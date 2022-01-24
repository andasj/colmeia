from flask import Flask, jsonify, Response
import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)  # Iniciar a captcao

    def __del__(self):
        self.video.release()  # Liberar a webCam

    def get_frame(self):
        ret, frame = self.video.read()
        # frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        return frame

def choice_face(image, faces_detectadas):

    # Inicializa as variaveis
    face_detectada = faces_detectadas[0]
    area_face = face_detectada[2]*face_detectada[3]

    # Loop para encontrar rosto com maior área na imagem.
    for index, (x, y, l, a) in enumerate(faces_detectadas):
        if l*a > area_face:
            area_face = l*a
            face_detectada = (x, y, l, a)

    # Marcando na imagem a região do rosto encontrada.
    (x, y, l, a) = face_detectada
    cv2.rectangle(image, (x, y), (x + l, y + a), (0, 0, 255), 7)

    return image

def detect_face(image):
    # Carregando o classificador
    classificador = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Convertendo para cinza
    image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detectando faces no frame
    faces_detectadas = classificador.detectMultiScale(image_grayscale, scaleFactor=1.1, minNeighbors=16)  # parâmetros principais
    # scaleFactor: Parâmetro que especifica o quanto o tamanho da imagem é reduzido em cada escala de imagem.
    # minNeighbors: Parâmetro que especifica quantos vizinhos cada retângulo candidato deve ter para retê-lo.

    if len(faces_detectadas) > 0:
        # Marcando na imagem o maior rosto encontrado
        image = choice_face(image, faces_detectadas)

        # Using cv2.putText() method
        image = cv2.putText(image, 'Face frontal detected!!!', (35, 35), cv2.FONT_ITALIC, 1, (0, 255, 0), 5, cv2.LINE_AA)
        return True, image

    # Preparando a imagem para caso o algoritmo não encontre faces na imagem
    image = cv2.merge((image_grayscale, image_grayscale, image_grayscale))
    image = cv2.putText(image, 'Face frontal not detected!!!', (35, 35), cv2.FONT_ITALIC, 1, (0, 0, 255), 5, cv2.LINE_AA)
    return False, image

def main():

    webcam = VideoCamera()
    frame = webcam.get_frame()
    result, frame_result = detect_face(frame)

    return result, frame_result

app = Flask(__name__)

@app.route('/')
def index():
    return 'Desafio Colmeia!!!!'

@app.route('/json')
def initial_test():

    result, frame_result = main()

    return jsonify({'Face detect': result})

@app.route('/image')
def show_image():

    result, frame_result = main()

    data = cv2.imencode('.png', frame_result)[1].tobytes()
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')

def main():

    webcam = VideoCamera()
    frame = webcam.get_frame()
    result, frame_result = detect_face(frame)

    return result, frame_result

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=81)
    app.run()
