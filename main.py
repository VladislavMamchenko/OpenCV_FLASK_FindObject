import cv2
from flask import Flask, request, make_response, render_template
import base64
import numpy as np
import urllib

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

def Filter_Fudiao(src_img):
    # filter=np.array([[-1,0,0],[0,0,0],[0,0,1]])
    filter = np.array([[-1, 0], [0, 1]])
    row=src_img.shape[0]
    col=src_img.shape[1]
    new_img=np.zeros([row,col],dtype=np.uint8)
    for i in range(row-1):
        for j in range(col-1):
            new_value = np.sum(src_img[i:i + 2, j:j + 2] * filter) + 128  # point multiply
            if new_value > 255:
                new_value = 255
            elif new_value < 0:
                new_value = 0
            else:
                pass
            new_img[i, j]=new_value
    return new_img

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
    hsv_min = np.array((2, 28, 65), np.uint8)
    hsv_max = np.array((26, 238, 255), np.uint8)

    before_img = cv2.imread('images/1.jpg')

    #переведення картинки в сірий
    imgray = cv2.cvtColor(before_img, cv2.COLOR_BGR2GRAY)
    #маніпулятор ТРЕШ
    thresh = 170
    #бінарізація + маніпулятори(агрументи трешхолд)
    ret, thresh = cv2.threshold(imgray,thresh, 255, 0)
    #Знаходимо контури
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #пусте зображення для контурів
    img_contours = np.zeros(before_img.shape)

    #малюємо контури на пустому зображенні
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)


    #виведення вихідного зображення
    output_img = thresh
    retval, buffer = cv2.imencode('.jpg', output_img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'



    return response


if __name__ == '__main__':
    app.run(debug=True)


