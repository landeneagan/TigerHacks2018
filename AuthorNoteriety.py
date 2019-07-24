import requests

#https://www.googleapis.com/customsearch/v1?key=AIzaSyAT3PKpgtjWdjHBemeHT5ZkDbwnZBARBEE&cx=011809875003834266328:_eunbtqpsiq&q= 

#input: author's name
#append to URL
#Make GET request for search
#Look at all those pages and see if they are articles
#For every article, bump Classifier

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

    for i in range(0,len(data['items'])):
        #print(data['items'][i]['link'])
        search = 'https://api.aylien.com/api/v1/extract?url=' + data['items'][i]['link']
        linkReq = requests.get(url = search, headers=headers) 
        authorData = linkReq.json()
        #print(authorData['author'])
        if( authorName == authorData['author'] ): #might want to check if api finds multiple authors
            noteriety += 1
        
    return noteriety

print(AuthorNoteriety('Lizette Alvarez'))