import cv2
from flask import Flask, request, make_response, render_template
import base64
import numpy as np
import urllib

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/downloaded_photo')
def downloaded_photo():
    img = cv2.imread('images/1.jpg')
    myimg = cv2.imshow(img)
    return myimg


if __name__ == '__main__':
    app.run(debug=True)


