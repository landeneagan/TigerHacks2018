# import tensorflow as tf
# from tensorflow import keras
from textblob import TextBlob
import numpy as np
import requests
import articleDateExtractor
import sqlalchemy
import os
from stop_words import get_stop_words
import logging
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)

# import pymysql.cursors
# Environment variables are defined in app.yaml.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app = Flask(__name__)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

def Parser( url ):
    
    search = 'https://api.aylien.com/api/v1/extract?url=' + url

    headers = {
        "X-AYLIEN-TextAPI-Application-ID":"f94984be",
        "X-AYLIEN-TextAPI-Application-Key":"83a7b904239577d9967e5402c461f388"
    }

    req = requests.get(url = search, headers=headers) 
    data = req.json()

    date = articleDateExtractor.extractArticlePublishedDate(url)

    formattedDate = date
    if( date != None ):
        formattedDate = str(date).replace("-", "")
        formattedDate = formattedDate[:-9]
        formattedDate = int(formattedDate)

    parsed = {
        'title': data['title'],
        'author': data['author'],
        'article': data['article'],
        'date': formattedDate
    }

    return parsed

def DateResearchValue( date, keywords ):
    #date needs to be in format -> 20140815:20140931
    #keywords can be a string with words seperated by spaces, I guess
    dateValue = 0
    url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyAT3PKpgtjWdjHBemeHT5ZkDbwnZBARBEE&cx=011809875003834266328:_eunbtqpsiq&q='
    search = url
    for i in range(1,len(keywords)):    
        search = search + keywords[i] + ' '
    dateBefore = date - 10000
    dateAfter = date + 10000 
    search = search + '&sort=date:r:' + str(dateBefore) + ':' + str(dateAfter) 

    req = requests.get(url = search, params = None)
    data = req.json()

    for i in range(0,len(data['items'])):
        print(data['items'][i]['title'])
        matches = list(set(return_keywords(data['items'][i]['title'])).intersection(keywords))
        if ( len(matches) > 1 ):
                dateValue += 1

    return dateValue

def Polarity(string):
    sentiment = TextBlob(string)
    return sentiment.sentiment.polarity

def return_keywords(headline):	
    headline = headline.lower()
    stop_words = set(get_stop_words('en'))
    word_tokens = headline.split() 
    filtered_sentence = []
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w)
    return filtered_sentence

def AuthorNoteriety( authorName ):
    noteriety = 0
    url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyAT3PKpgtjWdjHBemeHT5ZkDbwnZBARBEE&cx=011809875003834266328:_eunbtqpsiq&q='
    search = url + authorName

    req = requests.get(url = search, params = None)
    data = req.json()

    headers = {
        "X-AYLIEN-TextAPI-Application-ID":"f94984be",
        "X-AYLIEN-TextAPI-Application-Key":"83a7b904239577d9967e5402c461f388"
    }

    for i in range(1,len(data['items'])):
        #print(data['items'][i]['link'])
        search = 'https://api.aylien.com/api/v1/extract?url=' + data['items'][i]['link']
        linkReq = requests.get(url = search, headers=headers) 
        authorData = linkReq.json()
        #print(authorData['author'])
        if( authorName == authorData['author'] ): #might want to check if api finds multiple authors
            noteriety += 1
        
    return noteriety

def SourceValidation(url):

    url.replace("https://","")
    url.replace("http://","")

    endIndex = url.index("/")
    endOfUrl = len(url) - 1
    url[:-(endOfUrl - endIndex)]

    httpUrl = 'http://' + url
    httpsUrl = 'https://' + url

    #connection = pymysql.connect(host='35.239.255.99', user='root', password='password', db='source_validation', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    #cursor = db.cursor()
    # db.Model.query.
    for score in db.Model.query('urls').filter(or_(url==httpsUrl, url==httpUrl)):
        print(score)
        send = score

    # with connection.cursor() as cursor:
    #     sql = "SELECT `score` FROM `urls` WHERE `url` = %s OR `url` = %s"
    #     cursor.execute(sql, (httpUrl, httpsUrl,))
    #     score = cursor.fetchone()
    #     print(score)
    # connection.close()

    return send

def Decider():
    #given ratings from the classifier, use Machine Learning Magic to determine if fake news
    model = keras.models.Sequential()
    # Adds a densely-connected layer with 64 units to the model:
    #model.add(keras.layers.Dense(64, kernel_regularizer=keras.regularizers.l1(0.01))
    # Add another:
    model.add(keras.layers.Dense(64, input_shape=(32,), activation='sigmoid'))
    # Adds another
    model.add(keras.layers.Dense(64, activation='relu'))
    # Add another:
    model.add(keras.layers.Dense(64, activation='relu'))
    # Add a softmax layer with 1 output unit:
    model.add(keras.layers.Dense(1, activation='softmax')) 

    model.compile(optimizer=keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    data = np.random.random((1000, 32))
    labels = np.random.random((1000, 1))

    val_data = np.random.random((100, 32))
    val_labels = np.random.random((100, 1))

    callbacks = [
        # Interrupt training if `val_loss` stops improving for over 2 epochs
        keras.callbacks.EarlyStopping(patience=5, monitor='val_loss'),
        # Write TensorBoard logs to `./logs` directory
        keras.callbacks.TensorBoard(log_dir='./logs')
    ]

    model.fit(data, labels, epochs=10, callbacks=callbacks, batch_size=32, validation_data=(val_data, val_labels))
    model.save('./FIND-model.h5')
    # model = keras.models.load_model('FIND-model.h5')
    # ^^^ to load a saved model

    return 0

#def FIND():
    #call Parser
    #call Classifier
    #call Decider
    
@app.route('/')
def main():
    print('start')
    sentUrl = request.args.get('url')
    #sentUrl = 'https://www.cnet.com/news/google-plus-and-life-after-social-media-death/'
    info = Parser(sentUrl)

    #sourceRating = sourceRater(sentUrl)
    authorRating = AuthorNoteriety(info['author'])
    articlePolarity = Polarity(info['article'])
    titlePolarity = Polarity(info['title'])
    dateRating = 0
    if( info['date'] != None ):
        dateRating = DateResearchValue(info['date'], return_keywords(info['title']))

    print(info)
    print(authorRating)
    print(articlePolarity)
    print(titlePolarity)
    print(dateRating)
    print('sourceRating')
    return print(SourceValidation('https://www.cnet.com/news/google-plus-and-life-after-social-media-death/'))
    #x = Decider()
    # print("we did it")

    #return 'success'

# main()