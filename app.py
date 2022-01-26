from flask import Flask, jsonify, Response
import cv2
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def main():

    camera = cv2.VideoCapture(0)
    success_frame, frame = camera.read()

    if not success_frame:
        frame = cv2.imread('upload/image.jpg')

    result, frame_result = detect_face(frame)

    return result, frame_result

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return 'Desafio Colmeia!!!!'

@app.route('/json')
def show_json():

    result, frame_result = main()
    shape_image = frame_result.shape

    return jsonify({'Face detect': result, 'Shape image': shape_image})

@app.route('/image')
def show_image():

    result, frame_result = main()
    data = cv2.imencode('.png', frame_result)[1].tobytes()
    return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = 'image.jpg'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     filename = 'image.jpg'
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     print(file)
        #     print(filename)
        #     print(os.path.join(app.config['UPLOAD_FOLDER']))
        #     # return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
