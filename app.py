import base64
from calendar import c
from io import BytesIO
import string
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # allow cross-origin requests


def splitCaptionsIntoParts(captions):
    """
        Split captions into parts, so that they can be displayed in multiple lines.
        Returns a list of lists, where each list contains the captions for one line.
    """
    top = captions[:len(captions)//2]
    bottom = captions[len(captions)//2:]
    bottom = bottom.split(" ")
    top+= bottom[0]
    bottom = " ".join(bottom[1:])
    captions = [top, bottom]
    n_words = [len(caption.split()) for caption in captions]
    new_text = " ".join(captions)
    
    new_text = new_text.split()
    new_captions = list()
    pos = 0
    for _, ctr in enumerate(n_words):
        new_captions.append(" ".join(new_text[pos: pos + ctr]))
        pos += ctr

    new_captions_dict = dict()
    new_captions_dict['top'] = new_captions[0]
    new_captions_dict['bottom'] = new_captions[1]
    return new_captions_dict

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/gen', methods=['GET', 'POST'])
def generateImage():
    if request.method == 'POST': 
        # ! idk, for some reason even with CORS enabled, GET requests are not allowed

        # read body of request
        content = request.get_json()
        captions = content['caption']
        captions = splitCaptionsIntoParts(captions)

        img_base64 = content['img_base64']
        img_base64 = img_base64.split(",")[1]
        # create image from base64
        
        img = Image.open(BytesIO(base64.b64decode(img_base64)))
        # add text to image
        for position, caption in list(captions.items()):
            addText(img, position, caption)

        # render the image on the browser
        # So save the image to a buffer, and send it back as a base64 string
        img.save('img/meme.png')
        img_base64 = base64.b64encode(open('img/meme.png', 'rb').read())
        img_base64 = img_base64.decode('utf-8')
        return jsonify({"img_base64": img_base64})


def addText(img, pos, msg):
    fontSize = 56
    lines = []

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("impact.ttf", fontSize)
    # font = ImageFont.load_default()
    w, h = draw.textsize(msg, font)

    imgwithpadding = img.width * 0.99

    line_C = 1
    if(w > imgwithpadding):
        line_C = int(round((w / imgwithpadding) + 1))

    if line_C > 2:
        while True:
            fontSize -= 2
            fnopen = open("impact.ttf", "rb")
            font = ImageFont.truetype(fnopen, fontSize)
            w, h = draw.textsize(msg, font)
            line_C = int(round((w / imgwithpadding) + 1))
            fnopen.close()
            if line_C < 3 or fontSize < 10:
                break

    lastCut = 0
    isLast = False
    for i in range(0, line_C):
        if lastCut == 0:
            cut = (len(msg) / line_C) * i
        else:
            cut = lastCut

        if i < line_C-1:
            nextCut = (len(msg) / line_C) * (i+1)
        else:
            nextCut = len(msg)
            isLast = True

        cut = int(cut)
        nextCut = int(nextCut)

        if nextCut == len(msg) or msg[nextCut] == " ":
            pass
        else:
            while msg[nextCut] != " ":
                nextCut += 1

        line = msg[cut:nextCut].strip()

        w, h = draw.textsize(line, font)
        if not isLast and w > imgwithpadding:
            nextCut -= 1
            while msg[nextCut] != " ":
                nextCut -= 1

        lastCut = nextCut
        lines.append(msg[cut:nextCut].strip())

    lastY = -h
    if pos == "bottom":
        lastY = img.height - h * (line_C+1) - 10

    for i in range(0, line_C):
        w, h = draw.textsize(lines[i], font)
        textX = img.width/2 - w/2
        textY = lastY + h
        draw.text((textX-2, textY-2), lines[i], (0, 0, 0), font=font)
        draw.text((textX+2, textY-2), lines[i], (0, 0, 0), font=font)
        draw.text((textX+2, textY+2), lines[i], (0, 0, 0), font=font)
        draw.text((textX-2, textY+2), lines[i], (0, 0, 0), font=font)
        draw.text((textX, textY), lines[i], (255, 255, 255), font=font)
        lastY = textY

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='