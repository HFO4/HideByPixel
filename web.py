# -*- coding: UTF-8 -*-

import random

from PIL import Image
from flask import render_template, Flask, request, send_from_directory
from numpy import *

ab_path = os.path.split(os.path.realpath(__file__))[0]


def dec2bin(str_num):
    num = int(str_num)
    bit = []
    while True:
        if num == 0:
            break
        num, rem = divmod(num, 2)
        bit.append(str(rem))
    return ''.join(bit[::-1])


def text2bin(foo):
    t = ""
    for i in range(len(foo)):
        t = t + str(dec2bin(str(ord(foo[i]))).zfill(16))
    return t


def bin2dec(string_num):
    return str(int(string_num, 2))


def bringback(foo):
    t = ""
    count = 0
    text = ""
    for i in range(len(foo)):
        t = t + foo[i]
        count = count + 1
        if count == 16:
            text = text + chr(int(bin2dec(t)))
            t = ""
            count = 0
    return text


def ling(im):
    if im == 0:
        return im + 1
    elif jiou(im):
        return im + 1
    else:
        return im


def o(im):
    if im == 255:
        return im - 1
    elif jiou(im):
        return im
    else:
        return im - 1


def jiou(num):
    if (num % 2) == 0:
        return True
    else:
        return False


def han(filename, t):
    foo = "00000000000000000" + text2bin(t) + "11111111111111111"
    print(foo)
    strLen = len(foo)
    imm = Image.open(ab_path + "/file/" + filename)
    im = array(imm)
    count = 0
    for i in range(0, imm.size[1] - 1):
        for y in range(0, imm.size[0] - 1):
            for x in range(0, 3):
                if count > strLen - 1:
                    break
                if foo[count] == "0":
                    im[i, y, x] = ling(im[i, y, x])
                else:
                    im[i, y, x] = o(im[i, y, x])
                count = count + 1
    tt = Image.fromarray(im)
    tt.save(ab_path + "/file/" + filename + "_result.png")


def readImg(filename):
    imm = Image.open(ab_path + "/file/" + filename)
    im = array(imm)
    count = 0
    t = ""
    check = 0
    for i in range(0, imm.size[1] - 1):
        for y in range(0, imm.size[0] - 1):
            for x in range(0, 3):
                if check == 17:
                    break
                if jiou(im[i, y, x]):
                    t = t + "1"
                else:
                    t = t + "0"
                check = check + 1
    if t == "00000000000000000":
        t = ""
        for i in range(0, imm.size[1] - 1):
            for y in range(0, imm.size[0] - 1):
                for x in range(0, 3):
                    if count == 17:
                        break
                    if jiou(im[i, y, x]):
                        t = t + "1"
                        count = count + 1
                    else:
                        t = t + "0"
                        count = 0
        return bringback(t[17:-16])
    else:
        return "未读取到结果"


# importlib.reload(sys)
# sys.setdefaultencoding('utf-8')
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


@app.route('/')
def hello_world():
    return render_template('up.html')


@app.route('/read')
def read():
    return render_template('read.html')


@app.route('/request', methods=['GET', 'POST'])
def req():
    if request.method == 'POST':
        fileName = ''
        t = ''
        try:
            t = request.form['t']
            f = request.files['upload']
            fileName = str(random.randint(1, 1000000000))
            f.save(ab_path + '/file/' + fileName)
        except:
            return render_template('info.html', meg="Something Happend...")
        finally:
            try:
                han(fileName, t)
                return send_from_directory(ab_path + "/file/", fileName + "_result.png", as_attachment=True)
            except:
                return render_template('info.html', meg="无法处理请求，请检查你的输入和图片合法性")
    else:
        return '<h1>bad req</h1>'


@app.route('/read_handle', methods=['GET', 'POST'])
def req_r():
    if request.method == 'POST':
        fileName = ''
        try:
            f = request.files['upload']
            fileName = str(random.randint(1, 1000000000))
            f.save(ab_path + '/file/' + fileName)
        except:
            return render_template('info.html', meg="Something Happend...")
        finally:
            try:
                return render_template('success.html', meg=readImg(fileName))
            except:
                return render_template('info.html', meg="无法处理请求，图片可能已损坏")
    else:
        return '<h1>bad req</h1>'


if __name__ == '__main__':
    app.run(debug=True)
