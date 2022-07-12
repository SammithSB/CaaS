import base64
from io import BytesIO
import random
import string
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def createMeme(captions):
    captions = convertCaptionsCamelCase(captions)
    try:
        if(captions['top'] == captions['bottom'] == ''):
            raise ValueError
        filename = generateImage(captions)
    except ValueError as e:
        print(f"Bad request: {str(e)}")
        filename = handleErrorMeme()

    return filename


def handleErrorMeme():
    caption_choices = [
        {'top': "i know how to", 'bottom': "make memes"},
        {'top': '', 'bottom': "i can make memes bro"},
        {'top': "i am a professional", 'bottom': "meme maker"},
        {'top': "my meme game", 'bottom': "is strong"},
        {'top': "i know how to", 'bottom': "use saas"}
    ]
    captions = random.choice(caption_choices)
    filename = createMeme(captions)
    return filename


def convertCaptionsCamelCase(captions):
    print(captions)
    # captions = captions
    top = captions[:len(captions)//2]
    bottom = captions[len(captions)//2:]
    bottom = bottom.split(" ")
    top+= bottom[0]
    bottom = " ".join(bottom[1:])
    captions = [top, bottom]
    n_words = [len(caption.split()) for caption in captions]
    text = " ".join(captions)
    new_text = str()
    flag = False
    for ch in text:
        if ch in string.ascii_letters:
            if flag:
                new_text += ch
                flag = False
            else:
                new_text += ch
                flag = True
        else:
            new_text += ch

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
    print(request.method)


    if 1 == 1: 
        # read body of request
        content = request.get_json()
        print(content)
        # return "jjj"
        captions = content['caption']
        captions = convertCaptionsCamelCase(captions)
        print(captions)
        # return "kkkk"
        img_base64 = content['img_base64']
        img_base64 = img_base64.split(",")[1]
        # create image from base64
        img = Image.open(BytesIO(base64.b64decode(img_base64)))
        # render the image with a popup
        img.save('img/meme.png')
        
        for position, caption in list(captions.items()):
            addText(img, position, caption)

        # render the image on the browser
        img.save('img/meme.png')
        img_base64 = base64.b64encode(open('img/meme.png', 'rb').read())
        img_base64 = img_base64.decode('utf-8')
        return jsonify({"img_base64": img_base64})

        # captions = [c for c in captions.values() if c.strip() != ""]
        # filename = "-".join(captions)+".jpg"
        # filename = filename.replace(' ', '-')
        # img.save("img/final.png")
        # # img.close()
        # # return filename
        # # encode image to base64
        # img_base64 = base64.b64encode(open("img/final.png", "rb").read())
        # img_base64 = img_base64.decode("utf-8")
        # print(img_base64)
        # # return jsonify({"img_base64": img_base64})
        # return render_template('index.html', img_base64=img)


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