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
    clear_con_img = np.ones(before_img.shape[:2], dtype="uint8") * 255
    #малюємо контури на чистому зображенні
    #передаємо чисте зображення,контур, ?? , колір , ?? (відповідає за товщину контура а з -1 за заливку
    filled_cont = cv2.drawContours(clear_con_img, [max_contour], -1, (0, 0, 255), -1)


    #"випалюємо" фон заданий маскою
    #betwise_(and/or/not) - побітові операції з зображеннями
    masked = cv2.bitwise_not(before_img, before_img, mask=filled_cont)





    #виведення вихідного зображення
    output_img = masked

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



    #виведення вихідного зображення
    output_img = clear_con_img

    retval, buffer = cv2.imencode('.jpg', output_img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'

    return response

@app.route('/output_photo5')
def output_photo5():


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
    # orig_with_cont = before_img
    # #малюємо контури на пустому зображенні
    # cv2.drawContours(orig_with_cont, contours, -1, (0, 255, 0), 3)

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


