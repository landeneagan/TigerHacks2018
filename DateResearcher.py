import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

def return_keywords(headline):	
	stop_words = set(stopwords.words('english'))
	word_tokens = word_tokenize(headline.lower()) 
	filtered_sentence = [w for w in word_tokens if not w in stop_words] 
	filtered_sentence = []
	for w in word_tokens: 
		if w not in stop_words: 
			filtered_sentence.append(w)
	return filtered_sentence

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
        #if( data['items'][i]['title'] has keywords ):
        # from ToneSensor, find keywords for this data
        # confirm intersection has 3+ keywords
        #if( 1==1 ):
        #    dateValue += 1

    return dateValue

testList = ["trump", "election", "russia", "colusion"]

print(DateResearchValue( 20180624, testList ))