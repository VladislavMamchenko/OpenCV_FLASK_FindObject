import cv2
from flask import Flask, request, make_response, render_template
import base64
import numpy as np
import imutils
from matplotlib import pyplot as plt
import python_utils
import urllib


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')



# вивід вхідного зображення
@app.route('/downloaded_photo')
def downloaded_photo():
    img = cv2.imread('images/1.jpg')
    retval, buffer = cv2.imencode('.jpg', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'
    return response

@app.route('/output_photo')
def output_photo():


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
    output_img = masked

    retval, buffer = cv2.imencode('.jpg', output_img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'



    return response


if __name__ == '__main__':
    app.run(debug=True)


