import cv2
from flask import Flask, request, make_response, render_template, flash, url_for,redirect
# import base64
import os
import urllib.request
from werkzeug.utils import secure_filename
import numpy as np
# import imutils
from matplotlib import pyplot as plt
# import python_utils
# import urllib
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired

# before_img = cv2.imread('images/1.jpg')
# result = before_img.copy()
# imgray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)
#
# limit_val = 100
#
# filtered = cv2.bilateralFilter(imgray, 11, 50, 100)
# ret, thresh = cv2.threshold(filtered, limit_val, 255, cv2.THRESH_BINARY)
#
# plt.hist(imgray.ravel(),256,[0,256])
# plt.axvline(x = limit_val, color = 'b', label = 'limit value')
#
# plt.savefig('images/saved_figure.jpg')




app = Flask(__name__)

UPLOAD_FOLDER = 'images/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

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
        flash('Allowed image types are - png, jpg, jpeg, gif')
    return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)




# вивід вхідного зображення
@app.route('/downloaded_photo', methods=['GET', 'POST'])
def downloaded_photo():

    img = cv2.imread('images/1.jpg')
    retval, buffer = cv2.imencode('.jpg', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'
    return response



# @app.route('/', methods=['POST'])
# def my_form_post():
#
#     slider1value = request.form['slider1']
#     slider2value = request.form['slider2']
#     slider3value = request.form['slider3']
#     slider4value = request.form['slider4']
#     slider5value = request.form['slider5']
#     return slider1value, slider2value, slider3value, slider4value, slider5value

@app.route('/edit_value', methods=["POST"])
def edit_img():

    slider1value = request.form.get('slider1')
    # slider2value = request.form.get('#ID_NAME')
    # slider3value = request.form.get('#ID_NAME')
    # slider4value = request.form.get('#ID_NAME')
    # slider5value = request.form['slider5']
    ### YOUR CODE
    return render_template('index.html')
    # return render_template('index.html', result = request.form)



@app.route('/output_photo', methods=['post', 'get'])
def output_photo():


    # val1 = request.args.get('param1')
    # val2 = request.args.get('param2')
    # val3 = request.args.get('param3')
    # val4 = request.args.get('param4')
    # val5 = request.args.get('param5')


    before_img = cv2.imread('images/1.jpg')
    result = before_img.copy()
    # переведення картинки в сірий
    imgray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)

    # фільтруємо зображення(можно також використати розмиття)
    # параметри (зображення(сіре), діаметр(скільки пікселів буде охоплено),цвітовий вимір(як багато пікселів з однаковим кольором будуть змішуватися,координатний вимір
    # (як багато пікселів будуть змішуватися,які будуть схожі за координатами)
    filtered = cv2.bilateralFilter(imgray, 11, 50, 100)

    # пошук країв зображення методом Кенні

    # маніпулятор ТРЕШ порогове значення
    # бінарізація + маніпулятори(агрументи трешхолд)
    # Також thresh виступає як маска
    ret, thresh = cv2.threshold(filtered, 100, 255, 0)

    # пошук країв методом Кенні
    edges = cv2.Canny(filtered, 30, 100)

    # Знаходимо контури
    # Параметри (зображення,режим знаходження контурів(RETR_TREE - ієрархічний порядок контурів),метод знаходження контурів(сімпл більш оптимізований))
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    max_contour = []

    # шукаємо найбільший контур
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.001 * cv2.arcLength(cnt, True), True)

        cnt_area = cv2.contourArea(cnt)
        # перевіряємо кількість точок
        # Інакше можливо що найбільшим контуром буде трикутник через все зображення
        if len(approx) > 3 and cnt_area > max_area:
            max_area = cnt_area
            max_contour = approx





    mask = np.zeros_like(before_img)
    cv2.drawContours(mask, [max_contour], -1, (255, 255, 255), -1)
    out = np.zeros_like(before_img)  # Extract out the object and place into output image
    out[mask == 255] = before_img[mask == 255]

    # виведення вихідного зображення
    output_img = out



    retval, buffer = cv2.imencode('.png', output_img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'

    return response

@app.route('/output_photo1')
def output_photo1():


    before_img = cv2.imread('images/1.jpg')


    # Кількісно визначаємо кольори
    # before_img = _utils.quantify_colors(img_small, 32, 10)

    #переведення картинки в сірий
    imgray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)


    #фільтруємо зображення(можно також використати розмиття)
    #параметри (зображення(сіре), діаметр(скільки пікселів буде охоплено),цвітовий вимір(як багато пікселів з однаковим кольором будуть змішуватися,координатний вимір
    #(як багато пікселів будуть змішуватися,які будуть схожі за координатами)
    filtered = cv2.bilateralFilter(imgray,11,50,100)

    #пошук країв зображення методом Кенні
    edges = cv2.Canny(filtered, 30, 100)

    #маніпулятор ТРЕШ порогове значення
    thresh = 100
    #бінарізація + маніпулятори(агрументи трешхолд)
    #Також thresh виступає як маска
    ret, thresh = cv2.threshold(filtered, thresh, 255, 0)
    #Знаходимо контури
    #Параметри (зображення,режим знаходження контурів(RETR_TREE - ієрархічний порядок контурів),метод знаходження контурів(сімпл більш оптимізований))
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #зчитуємо контури за домоголою бібліотеки imutils
    #all_contours = imutils.grab_contours(contours.copy())


    #якщо закоментувати,то на виході буде вирізане зображення без контурів
    orig_with_cont = before_img
    #малюємо контури на пустому зображенні
    cv2.drawContours(orig_with_cont, contours, -1, (0, 255, 0), 3)

    #"випалюємо" фон заданий маскою
    #betwise_(and/or/not) - побітові операції з зображеннями
    masked = cv2.bitwise_and(before_img, before_img, mask=thresh)
    masked[thresh < 2] = [255, 255, 255]

    #виведення вихідного зображення
    output_img = imgray

    retval, buffer = cv2.imencode('.jpg', output_img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'



    return response

@app.route('/output_photo2')
def output_photo2():


    before_img = cv2.imread('images/1.jpg')


    # Кількісно визначаємо кольори
    # before_img = _utils.quantify_colors(img_small, 32, 10)

    #переведення картинки в сірий
    imgray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)


    #фільтруємо зображення(можно також використати розмиття)
    #параметри (зображення(сіре), діаметр(скільки пікселів буде охоплено),цвітовий вимір(як багато пікселів з однаковим кольором будуть змішуватися,координатний вимір
    #(як багато пікселів будуть змішуватися,які будуть схожі за координатами)
    filtered = cv2.bilateralFilter(imgray,11,50,100)

    #маніпулятор ТРЕШ порогове значення
    thresh = 100
    #бінарізація + маніпулятори(агрументи трешхолд)
    #Також thresh виступає як маска
    ret, thresh = cv2.threshold(filtered, thresh, 255, 0)


    #пошук країв методом Кенні
    edges = cv2.Canny(thresh, 30, 100)

    #Знаходимо контури
    #Параметри (зображення,режим знаходження контурів(RETR_TREE - ієрархічний порядок контурів),метод знаходження контурів(сімпл більш оптимізований))
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #зчитуємо контури за домоголою бібліотеки imutils
    #all_contours = imutils.grab_contours(contours.copy())


    #якщо закоментувати,то на виході буде вирізане зображення без контурів
    orig_with_cont = before_img
    #малюємо контури на пустому зображенні
    cv2.drawContours(orig_with_cont, contours, -1, (0, 255, 0), 3)

    #"випалюємо" фон заданий маскою
    #betwise_(and/or/not) - побітові операції з зображеннями
    masked = cv2.bitwise_and(before_img, before_img, mask=thresh)
    masked[thresh < 2] = [255, 255, 255]

    #виведення вихідного зображення
    output_img = edges

    retval, buffer = cv2.imencode('.jpg', output_img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'



    return response

@app.route('/output_photo3')
def output_photo3():


    before_img = cv2.imread('images/1.jpg')


    # Кількісно визначаємо кольори
    # before_img = _utils.quantify_colors(img_small, 32, 10)

    #переведення картинки в сірий
    imgray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)


    #фільтруємо зображення(можно також використати розмиття)
    #параметри (зображення(сіре), діаметр(скільки пікселів буде охоплено),цвітовий вимір(як багато пікселів з однаковим кольором будуть змішуватися,координатний вимір
    #(як багато пікселів будуть змішуватися,які будуть схожі за координатами)
    filtered = cv2.bilateralFilter(imgray,11,50,100)

    #пошук країв зображення методом Кенні
    edges = cv2.Canny(filtered, 30, 100)



    #маніпулятор ТРЕШ порогове значення
    thresh = 100
    #бінарізація + маніпулятори(агрументи трешхолд)
    #Також thresh виступає як маска
    ret, thresh = cv2.threshold(filtered, thresh, 255, 0)
    #Знаходимо контури
    #Параметри (зображення,режим знаходження контурів(RETR_TREE - ієрархічний порядок контурів),метод знаходження контурів(сімпл більш оптимізований))
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #зчитуємо контури за домоголою бібліотеки imutils
    #all_contours = imutils.grab_contours(contours.copy())


    #якщо закоментувати,то на виході буде вирізане зображення без контурів
    orig_with_cont = before_img
    #малюємо контури на пустому зображенні
    cv2.drawContours(orig_with_cont, contours, -1, (0, 255, 0), 3)

    #"випалюємо" фон заданий маскою
    #betwise_(and/or/not) - побітові операції з зображеннями
    masked = cv2.bitwise_and(before_img, before_img, mask=thresh)
    masked[thresh < 2] = [255, 255, 255]

    #виведення вихідного зображення
    output_img = thresh

    retval, buffer = cv2.imencode('.jpg', output_img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'



    return response

@app.route('/output_photo4')
def output_photo4():

    before_img = cv2.imread('images/1.jpg')


    # Кількісно визначаємо кольори
    # before_img = _utils.quantify_colors(img_small, 32, 10)

    #переведення картинки в сірий
    imgray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)


    #фільтруємо зображення(можно також використати розмиття)
    #параметри (зображення(сіре), діаметр(скільки пікселів буде охоплено),цвітовий вимір(як багато пікселів з однаковим кольором будуть змішуватися,координатний вимір
    #(як багато пікселів будуть змішуватися,які будуть схожі за координатами)
    filtered = cv2.bilateralFilter(imgray,11,50,100)

    #пошук країв зображення методом Кенні
    edges = cv2.Canny(filtered, 30, 100)

    #маніпулятор ТРЕШ порогове значення
    thresh = 100
    #бінарізація + маніпулятори(агрументи трешхолд)
    #Також thresh виступає як маска
    ret, thresh = cv2.threshold(filtered, thresh, 255, 0)
    #Знаходимо контури
    #Параметри (зображення,режим знаходження контурів(RETR_TREE - ієрархічний порядок контурів),метод знаходження контурів(сімпл більш оптимізований))
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    max_contour = []

    # шукаємо найбільший контур
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.001 * cv2.arcLength(cnt, True), True)

        cnt_area = cv2.contourArea(cnt)
        # перевіряємо кількість точок
        # Інакше можливо що найбільшим контуром буде трикутник через все зображення
        if len(approx) > 3 and cnt_area > max_area:
            max_area = cnt_area
            max_contour = approx


    #створюємо чисте зображення з розмірами оригіналу
    clear_con_img = np.zeros(before_img.shape, np.uint8)
    #малюємо контури на чистому зображенні
    #передаємо чисте зображення,контур, ?? , колір , ?? (відповідає за товщину контура а в -1 за заливку
    cv2.drawContours(clear_con_img, [max_contour], -1, (0, 255, 0), -1)

    #"випалюємо" фон заданий маскою
    #betwise_(and/or/not) - побітові операції з зображеннями
    masked = cv2.bitwise_and(before_img, before_img, mask=thresh)
    masked[thresh < 2] = [255, 255, 255]

    histogram = cv2.imread('images/saved_figure.jpg')

    #виведення вихідного зображення
    output_img = histogram

    #виведення вихідного зображення
    output_img = clear_con_img

    retval, buffer = cv2.imencode('.jpg', output_img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'

    return response

@app.route('/output_photo5')
def output_photo5():



    before_img = cv2.imread('images/1.jpg')
    result = before_img.copy()
    imgray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)

    limit_val = 100

    filtered = cv2.bilateralFilter(imgray, 11, 50, 100)
    ret, thresh = cv2.threshold(filtered, limit_val, 255, cv2.THRESH_BINARY)

    plt.hist(imgray.ravel(), 256, [0, 256])
    plt.axvline(x=limit_val, color='b', label='limit value')

    plt.savefig('images/saved_figure.jpg')

    histogram = cv2.imread('images/saved_figure.jpg')

    #виведення вихідного зображення
    output_img = histogram

    retval, buffer = cv2.imencode('.jpg', output_img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'



    return response

if __name__ == '__main__':
    app.run(debug=True)


