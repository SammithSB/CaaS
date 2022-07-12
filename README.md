# SpongeBob-as-a-Service

Converting the SpongeBob Mocking Meme into a Service to redefine the meaning of SaaS.

<p align="center">
  <img src="app/static/readme-meme.jpg">
</p>

# How to use SaaS

SaaS is pretty simple to use, and aims to be the simplest (and only) SpongeBob service that exists. The base URL is ```https://spongebob-service.herokuapp.com/```. Captions can be passed in two ways.

## SaaS using Routes

SaaS memes can be generated using the following URL route formats:

* **Bottom caption**: This will insert a caption at the bottom of the image. 
    * Format: ```https://spongebob-service.herokuapp.com/<bottom caption>```

* **Top and Bottom captions**: This will insert a caption at the top and bottom of the image.
    * Format: ```https://spongebob-service.herokuapp.com/<top caption>/<bottom caption>```

## SaaS using Parameters

SaaS memes can also be generated using parameters passed in the URL. This method although slower, provides greater flexibility in setting the image positions.

You can choose to have both captions, or either one caption.

* **Both captions**: ```https://spongebob-service.herokuapp.com/q?top=<top caption>&bottom=<bottom caption>```

* **Top or Bottom caption**: 
  * Top caption: ```https://spongebob-service.herokuapp.com/q?top=<top caption>```
  * **Bottom caption**: ```https://spongebob-service.herokuapp.com/q?bottom=<bottom caption>```

## SaaS in a Script
You can even use SaaS in a script. Here is a simple example using Python.

```Python
>>> import requests
>>> from bs4 import BeautifulSoup
>>> 
>>> base_url  = "https://spongebob-service.herokuapp.com/"
>>> meme_url = "https://spongebob-service.herokuapp.com/yOu CaNnOt/CoDe MeMes"
>>> 
>>> response = requests.get(meme_url)
>>> 
>>> soup = BeautifulSoup(response.text, 'html.parser')
>>> img_tags = soup.find_all('img')
>>> 
>>> img_url = img_tags[0]["src"]
>>> img_url = base_url + img_url
>>> 
>>> response = requests.get(img_url)
>>> with open("meme.jpg", 'wb') as outfile:
>>>     outfile.write(response.content)
```

# Inspiration to make Caption as a Service

PES 2023 biggest inspiration has always been Baral mama and this repo has taken his infamous Spongebob as a Service which was specific to Spongebob meme and converted it into more general any meme you want.

Feel free to contribute with more features or how to improve our code.
