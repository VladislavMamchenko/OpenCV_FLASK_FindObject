import cv2
from flask import Flask, request, make_response, render_template, flash, url_for, redirect, Response, jsonify
import os
import numpy as np
from matplotlib import pyplot as plt
import base64
import urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edit_page', methods=['GET'] )
def edit_page():
    return render_template('edit_page.html')

UPLOAD_FOLDER = 'images/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# метод завантаження користувацької картинки
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('Лише png, jpg,jpeg')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('Картинку не обрано')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], '1.jpg'))
        # print('upload_image filename: ' + filename)
        flash('Картинку завантажено успішно')
        return render_template('index.html', filename=filename)
    else:
        flash('Лише - png, jpg, jpeg')
    return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/processing', methods=['GET', 'POST'])
def processing():

    val1 = int(request.form.get('slider1'))
    val2 = int(request.form.get('slider2'))
    val3 = int(request.form.get('slider3'))
    val4 = int(request.form.get('slider4'))
    val5 = int(request.form.get('slider5'))

    val6 = int(request.form.get('radio'))

    before_img = cv2.imread('images/1.jpg')
    inverted_img = cv2.bitwise_not(before_img)

    if val6 == 1:
        working_img = cv2.bitwise_not(before_img)
    else:
        working_img = before_img




    result = before_img.copy()

    gray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(working_img, cv2.COLOR_BGR2GRAY)

    filtered = cv2.bilateralFilter(gray, val2, val3, val3)
    filtered2 = cv2.bilateralFilter(gray2, val2, val3, val3)

    edges = cv2.Canny(filtered, 30, 100)

    ret, thresh = cv2.threshold(filtered2, val1, 255, 0)

    # plt.hist(gray.ravel(), 256, [0, 256])
    # plt.axvline(110, color='b', label='limit value')
    #
    # plt.savefig('images/saved_figure.jpg')

    contours, hierarchy = cv2.findContours(thresh,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    max_contour = []

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.001 * cv2.arcLength(cnt, True), True)

        cnt_area = cv2.contourArea(cnt)
        if len(approx) > 3 and cnt_area > max_area:
            max_area = cnt_area
            max_contour = approx

    mask = np.zeros_like(before_img)
    cv2.drawContours(mask, [max_contour], -1, (255, 255, 255), -1)
    masked = cv2.drawContours(mask.copy(), [max_contour], -1, (1, 255, 1), -1)
    out = np.zeros_like(before_img)
    out[mask == 255] = before_img[mask == 255]

    output_img = out

    cv2.imwrite("images/gray.jpg", gray)
    cv2.imwrite("images/canny.jpg", edges)
    cv2.imwrite("images/filtered.jpg", filtered)
    cv2.imwrite("images/thresh.jpg", thresh)
    cv2.imwrite("images/out.jpg", output_img)
    cv2.imwrite("images/masked.jpg", masked)

    return render_template('edit_page.html')



@app.route('/downloaded_photo', methods=['GET', 'POST'])
def downloaded_photo():

    img = cv2.imread('images/1.jpg')

    retval, buffer = cv2.imencode('.jpg', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'
    return response

@app.route('/processed_photo', methods=['GET', 'POST'])
def processed_photo():

    img = cv2.imread('images/out.jpg')

    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/processed_photo1', methods=['GET', 'POST'])
def processed_photo1():

    img = cv2.imread('images/gray.jpg')

    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/processed_photo2', methods=['GET', 'POST'])
def processed_photo2():

    img = cv2.imread('images/canny.jpg')

    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/processed_photo3', methods=['GET', 'POST'])
def processed_photo3():

    img = cv2.imread('images/filtered.jpg')

    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/processed_photo4', methods=['GET', 'POST'])
def processed_photo4():

    img = cv2.imread('images/thresh.jpg')

    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/processed_photo5', methods=['GET', 'POST'])
def processed_photo5():

    img = cv2.imread('images/masked.jpg')

    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/diagram1', methods=['GET', 'POST'])
def diagram1():

    img = cv2.imread('images/saved_figure.jpg')

    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == '__main__':
    app.run(debug=True)


