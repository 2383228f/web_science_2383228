import pymongo
from pymongo import MongoClient
import json
import tweepy
import twitter
from pprint import pprint
import configparser
import pandas as pd
import string
import re

#### Access keys for twitter API ###
consumer_key = "KQrqB9MQV09JG1yxGRhfd1VfQ"
consumer_secret = "bhzIkAoynyLE9txF05fXYnmKsSdAWBrAZnhALmJVSTf2o4Xhuz"
access_token = "1352654452679970818-o5kJD6ueVwHz9NeRI1TRYktUk2CeiK"
access_token_secret = "9wxfiMh342LqVMiEcdqMdTvkv9iYC8ht6ifCENtLPTWEa"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

rest_auth = twitter.oauth.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
rest_api = twitter.Twitter(auth=rest_auth)
client = pymongo.MongoClient()

###Database information for MongoDB, along with label to add to each tweet entry ###
db = client.emotions
database = db.happyTweets 
label = "happy"


###Normalise function, takes in a string and returns a clean version 
def normalize(text):
    punctuation = "—!\"$%&'()*+, -./:;<=>?@[\]^_`{|}~" # Copy of punctuation without hashtag, so that full hashtags can still be removed after punctuation removed
    words = text.replace('\n',' ') # Removes newline characters
    words = re.sub(r'@[A-Za-z0-9]+','',words) # Removes @ mentions
    words = re.sub(r'RT[\s]+','',words) #Removes retweet tags
    words = words.replace(u'\xa0', u' ') #Some tweets contain character they shouldn't, changes to space
    words = words.split(" ") # Splits into array of words, delimited by space
    
    cleaned = []
    for word in words:
        word = re.sub("([a-z])\\1{3,}","\\1",word) # These find words like 'looooove' and transforms to 'love'
        word = re.sub("([A-Z])\\1{3,}","\\1",word)

        word = word.lower().strip() # Transforms to lower case and removes extraneous whitespace
        word = word.translate(str.maketrans('', '', punctuation)) # removes punctuation
        if word in contractions.keys():
            cleaned.append(contractions[word].lower()) # If contraction, adds lengthened version to clean array
            continue
        if not "http" in word and word != '' and '#' not in word: # Removes hyperlinks and hashtags
            cleaned.append(word)
    return cleaned


#Long dictionary for contractions
contractions = { #Tweeters are inconsisent with the characters that they use for contractions. As such, contractions using both ' and ’ are included in this dictionary. 
    "ain’t": "am not / are not",
    "aren’t": "are not / am not",
    "can’t": "cannot",
    "can’t’ve": "cannot have",
    "’cause": "because",
    "could’ve": "could have",
    "couldn’t": "could not",
    "couldn’t’ve": "could not have",
    "didn’t": "did not",
    "doesn’t": "does not",
    "don’t": "do not",
    "hadn’t": "had not",
    "hadn’t’ve": "had not have",
    "hasn’t": "has not",
    "'em":"them",
    "’em":"them",
    "haven’t": "have not",
    "he’d": "he had / he would",
    "he’d’ve": "he would have",
    "he’ll": "he shall / he will",
    "he’ll’ve": "he shall have / he will have",
    "he’s": "he has / he is",
    "how’d": "how did",
    "how’d’y": "how do you",
    "how’ll": "how will",
    "how’s": "how has / how is",
    "i’d": "I had / I would",
    "i’d’ve": "I would have",
    "i’ll": "I shall / I will",
    "i’ll’ve": "I shall have / I will have",
    "i’m": "I am",
    "i’m": "I am",
    "i’ve": "I have",
    "isn’t": "is not",
    "it’d": "it had / it would",
    "it’d’ve": "it would have",
    "it’ll": "it shall / it will",
    "it’ll’ve": "it shall have / it will have",
    "it’s": "it has / it is",
    "let’s": "let us",
    "ma’am": "madam",
    "mayn’t": "may not",
    "might’ve": "might have",
    "mightn’t": "might not",
    "mightn’t’ve": "might not have",
    "must’ve": "must have",
    "mustn’t": "must not",
    "mustn’t’ve": "must not have",
    "needn’t": "need not",
    "needn’t’ve": "need not have",
    "o’clock": "of the clock",
    "oughtn’t": "ought not",
    "oughtn’t’ve": "ought not have",
    "shan’t": "shall not",
    "sha’n’t": "shall not",
    "shan’t’ve": "shall not have",
    "she’d": "she had / she would",
    "she’d’ve": "she would have",
    "she’ll": "she shall / she will",
    "she’ll’ve": "she shall have / she will have",
    "she’s": "she has / she is",
    "should’ve": "should have",
    "shouldn’t": "should not",
    "shouldn’t’ve": "should not have",
    "so’ve": "so have",
    "so’s": "so as / so is",
    "that’d": "that would / that had",
    "that’d’ve": "that would have",
    "that’s": "that has / that is",
    "there’d": "there had / there would",
    "there’d’ve": "there would have",
    "there’s": "there has / there is",
    "they’d": "they had / they would",
    "they’d’ve": "they would have",
    "they’ll": "they shall / they will",
    "they’ll’ve": "they shall have / they will have",
    "they’re": "they are",
    "they’ve": "they have",
    "to’ve": "to have",
    "wasn’t": "was not",
    "we’d": "we had / we would",
    "we’d’ve": "we would have",
    "we’ll": "we will",
    "we’ll’ve": "we will have",
    "we’re": "we are",
    "we’ve": "we have",
    "weren’t": "were not",
    "what’ll": "what shall / what will",
    "what’ll’ve": "what shall have / what will have",
    "what’re": "what are",
    "what’s": "what has / what is",
    "what’ve": "what have",
    "when’s": "when has / when is",
    "when’ve": "when have",
    "where’d": "where did",
    "where’s": "where has / where is",
    "where’ve": "where have",
    "who’ll": "who shall / who will",
    "who’ll’ve": "who shall have / who will have",
    "who’s": "who has / who is",
    "who’ve": "who have",
    "why’s": "why has / why is",
    "why’ve": "why have",
    "will’ve": "will have",
    "won’t": "will not",
    "won’t’ve": "will not have",
    "would’ve": "would have",
    "wouldn’t": "would not",
    "wouldn’t’ve": "would not have",
    "y’all": "you all",
    "y’all’d": "you all would",
    "y’all’d’ve": "you all would have",
    "y’all’re": "you all are",
    "y’all’ve": "you all have",
    "you’d": "you had / you would",
    "you’d’ve": "you would have",
    "you’ll": "you shall / you will",
    "you’ll’ve": "you shall have / you will have",
    "you’re": "you are",
    "you’ve": "you have",
    "ain't": "am not / are not",
    "aren't": "are not / am not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had / he would",
    "he'd've": "he would have",
    "he'll": "he shall / he will",
    "he'll've": "he shall have / he will have",
    "he's": "he has / he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how has / how is",
    "i'd": "I had / I would",
    "i'd've": "I would have",
    "i'll": "I shall / I will",
    "i'll've": "I shall have / I will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it had / it would",
    "it'd've": "it would have",
    "it'll": "it shall / it will",
    "it'll've": "it shall have / it will have",
    "it's": "it has / it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had / she would",
    "she'd've": "she would have",
    "she'll": "she shall / she will",
    "she'll've": "she shall have / she will have",
    "she's": "she has / she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as / so is",
    "that'd": "that would / that had",
    "that'd've": "that would have",
    "that's": "that has / that is",
    "there'd": "there had / there would",
    "there'd've": "there would have",
    "there's": "there has / there is",
    "they'd": "they had / they would",
    "they'd've": "they would have",
    "they'll": "they shall / they will",
    "they'll've": "they shall have / they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had / we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what shall / what will",
    "what'll've": "what shall have / what will have",
    "what're": "what are",
    "what's": "what has / what is",
    "what've": "what have",
    "when's": "when has / when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where has / where is",
    "where've": "where have",
    "who'll": "who shall / who will",
    "who'll've": "who shall have / who will have",
    "who's": "who has / who is",
    "who've": "who have",
    "why's": "why has / why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had / you would",
    "you'd've": "you would have",
    "you'll": "you shall / you will",
    "you'll've": "you shall have / you will have",
    "you're": "you are",
    "you've": "you have"
}

#Count = number of tweets to return
count = 5 

###Search terms: to search, comment out words associated with target emotion to leave empty list and insert target hashtag into 'currentWords'
###Currently will search for 40 tweets using '#happiness'

happyWords = []#['#happiness','#joy', '#love','😂']
excitedWords = ['#excited','#excited','#cantwait','#excitedmuch']
angryWords = ['😠', '#angry','#outraged']#😠
pleasantWords = ['#goodvibes',"#nice",'#allgood', '#goodvibes'] #Music good differentiator between pleasant and happy
fearWords = ['#scared','#anxious','#nervous','😨']
surpriseWords = ['😞','#fail', '#ohwell','#disappointed']

currentWords = ['#happiness'] 
q = currentWords

#Creates list to remove any tweets that contain other emotion hashtags
otherWords = happyWords+excitedWords+angryWords+pleasantWords+fearWords+surpriseWords
for word in currentWords:
    try:
        otherWords.remove(word)
    except:
        continue

###Uses twitter API to crawl for tweets, tweet_mode must be extended to avoid truncation of tweet text
search_results = rest_api.search.tweets(count=count, q=q, lang='en', tweet_mode= 'extended')
statuses = search_results["statuses"]

for status in statuses:
    if 'full_text' in status.keys(): #Twitter api is inconsistent with its field names depending on how long the tweet was, so need to include code for both text and full_text
        textType = 'full_text'
    else:
        textType = 'text'

    #Stores clean representation of text and label in new fields in database
    status["clean"] = normalize(status[textType])
    status["label"] = label

    #Passes on tweets that contain other emotion tags
    for word in otherWords:
        if word in status[textType]:
            pass
    #Passes for duplicate values in database
    if database.count_documents({ textType: status[textType] }, limit = 1) == 0 and len(status[textType])>20:
        database.insert_one(status)
    else:
        pass
    


