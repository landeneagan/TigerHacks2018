import requests
import articleDateExtractor

def Parser( url ):

    search = 'https://api.aylien.com/api/v1/extract?url=' + url

    headers = {
        "X-AYLIEN-TextAPI-Application-ID":"f94984be",
        "X-AYLIEN-TextAPI-Application-Key":"83a7b904239577d9967e5402c461f388"
    }

    req = requests.get(url = search, headers=headers) 
    data = req.json()

    date = articleDateExtractor.extractArticlePublishedDate(url)
    #date = articleDateExtractor.extractArticlePublishedDate("http://techcrunch.com/2015/11/29/tyro-payments/")

    formattedDate = date
    #print(date)
    if( date != None ):
        formattedDate = str(date).replace("-", "")
        formattedDate = formattedDate[:-9]
        formattedDate = int(formattedDate)
        #print(formattedDate)

    parsed = {
        'title': data['title'],
        'author': data['author'],
        'article': data['article'],
        'date': formattedDate
    }

    return parsed

print(Parser('https://www.cnet.com/news/google-plus-and-life-after-social-media-death/'))