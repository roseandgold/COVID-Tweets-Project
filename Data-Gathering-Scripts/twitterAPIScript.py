'''
Takes a CSV of Tweet ids, accesses the Twitter API to get the Tweet text,
and returns a CSV with the date, text, location, language, hashtags, sentiment score and if it 
an original tweet or a re-tweet. The API call gathers up to 100 Tweets at a time.

Need to create a "tweet_data" folder so the script can output the CSVs to this folder.
Need to create a text file named "twitterApiSecrets.txt" which includes:
    {"token": <token>, "tokenSecret": <token Secret>, "consumerKey": <consumer key>, 
    "consumerSecret": <consumer secret}

Keyword arguments:
tweetIdFile -- filepath to a csv which contains the Tweet Ids and sentiment scores
nextTweet -- the index number of the Tweet in the file you want to start processing
             needs to be a multiple of 100
numTweet -- the number of Tweets you want to process, needs to be a multiple of 100

Laura Stagnaro, Ian Byrne
SIADS 591 & 592 Milestone I
Coronavirus Tweet Analysis Project
'''

# Import the necessary libraries
import tweepy
import json
import pandas as pd
import time
from collections import defaultdict
import sys
import os
    
def setupApi(tokenSecretFile):
    '''Sets up the Twitter API.
    
    Keyword arguments:
    tokenSecretFile -- a text file which contains a dictionary containing the token and consumer keys and secrets.
    
    Return:
    api -- the API connection object
    
    '''
    # Open the text file with the consumer and token information. Convert it to a json object
    with open(tokenSecretFile) as file: 
        tokenConsumerInfo = json.load(file)
    
    # Create the token and consumer variables
    token = tokenConsumerInfo['token']
    tokenSecret = tokenConsumerInfo['tokenSecret']
    consumerKey = tokenConsumerInfo['consumerKey']
    consumerSecret = tokenConsumerInfo['consumerSecret']
    
    # Connect to the Twitter Api
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(token, tokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    # Make sure connection to the API was successful
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    return api

def getTweetIds(tweetIdFile):
    '''Get the Tweet Ids to run through the Twitter Api as well as the sentiment scores for each Tweet.
    
    Keyword arguments:
    tweetIdFile -- csv filed which contains the Tweet id and sentiment score
    
    Return:
    tweetIdsList -- list of lists. Each list includes 100 tweet ids
    sentimentDict -- dictionary with the tweet ids as the key and sentiment score as the value
    
    '''
    # Create a dataframe with the tweet ids and sentiment scores
    tweetIdDf = pd.read_csv(tweetIdFile, header=None, names=['tweet_id', 'sentiment_score'])
    
    # Get a list of lists for the tweet ids. Each list contains 100 tweet ids
    tweetIds = tweetIdDf['tweet_id'].to_list()
    total100s = len(tweetIds)//100 # Get the number of lists of 100 tweet ids
    remainder = len(tweetIds) % 100 # This is the number of tweet ids which will be in the last list
    startEnd = zip(range(0, len(tweetIds)-remainder, 100),range(100, len(tweetIds), 100)) # Create a zip of tuples with what index to start and stop at to create the list of 100 tweet ids 
    tweetIdsList = [tweetIds[i:x] for i,x in startEnd] # Create the list of lists
    if remainder > 0:
        tweetIdsList.append(list(tweetIds[len(tweetIds)-remainder : len(tweetIds)])) # Append the last list
    
    # Create a dictionary which includes the tweet ids as the key and sentiment score as the value
    sentimentDict = dict(zip(tweetIdDf['tweet_id'].to_list(), tweetIdDf['sentiment_score'].to_list()))
    
    # Print out the number of Tweet ids in the list
    print('There are {} Tweet Ids'.format(len(tweetIdDf)))
    return tweetIdsList, sentimentDict

def parseTweet(tweetContent):
    '''Get the necessary information from the Tweet.
    
    Keyword argument:
    tweetContent -- tweet content in json format
    
    Return:
    idVal -- id value of the tweet
    timestamp -- timestamp of tweet
    text -- text content of the tweet
    hashtag -- hastags from the tweet
    location -- location of the user
    lang -- location of the tweet
    
    '''
    # Get the necessary information from the tweet content
    idVal = tweetContent.id # Get the id of the tweet
    timestamp = tweetContent.created_at # Returns a datetime timestamp
    location = tweetContent.user.location # Returns a string
    lang = tweetContent.lang # Get the language of the Tweet

    # Create a list with the hashtags
    hashtags = ''
    
    for tag in tweetContent.entities['hashtags']:
        hashtags = hashtags + tag['text'] + ", "

    # Get the tweet text
    if "retweeted_status" in tweetContent._json:
        text = tweetContent.retweeted_status.full_text
        status = 'Retweet'
    else:
            text = tweetContent.full_text # Returns a string
            status = 'Original'
    
    return idVal, timestamp, text, hashtags, location, lang, status


def main(tweetIdFile, nextTweet, numTweets):
    '''Create a dataframe which includes all the necessary Tweet information. The API searches for 100 tweet ids at
    one time.
    
    Keyword arguments:
    tweetIdFile -- a csv file with Tweet Ids and sentiment score
    tokenSecretFile -- a text file which includes a dictionary with Twitter token and consumer information
    nextTweet -- the next tweet you want to start at. Number needs to be multiple of 100.
    numTweets -- the number of Tweets to process. Number needs to be a multiple of 100 or can use "All" to process all Tweets
                from the nextTweet number to the end of list of Tweet ids.
    
    Return:
    twitterDf -- a dataframe with all necessary Twitter information
    
    '''
    # Create the variables
    nextTweet = int(nextTweet)
    numTweets = int(numTweets)
    tokenSecretFile = 'twitterApiSecrets.txt' # This needs to be a text file with a dictionary containing the keys: consumerKey, 
                                          # consumerSecret, token, and tokenSecret.
    
    # Get the Tweet Ids and sentiment scores
    tweetIds, sentimentDict = getTweetIds(tweetIdFile)
    
    # Setup the Twitter API
    api = setupApi(tokenSecretFile)
    
    # Create a default dictionary to hold all Tweet information
    tweetDict = defaultdict(list)
    
    # Iterate through the Tweet Ids
    start = int(nextTweet/100) # This indicates what group to start with
    if numTweets == "All":
        tweets = tweetIds[start:-1]
    else:
        numIterations = int(numTweets/100) # This is the number of groups of 100 tweet ids to search
        tweets = tweetIds[start:start + numIterations] # Get only the groups of tweets needed to process
    try:
        for idx, tweetGroup in enumerate(tweets):
            if idx % 100 == 0:
                rateLimitRemaining = api.rate_limit_status()['resources']['statuses']['/statuses/lookup']['remaining'] # Get the remaining rate limit
                print('Rate Limit Remaining: {}'.format(rateLimitRemaining)) # Print the rate limit remaining every 100 searches
            
            # Access the API and get the Tweet information
            tweetJson = api.statuses_lookup(tweetGroup, tweet_mode='extended') # Gets the json for all 100 tweets in the tweetGroup
            try: 
                # Iterate through each tweet json to get the information
                for tweet in tweetJson:
                    idVal, timestamp, text, hashtags, location, lang, status = parseTweet(tweet)
                    tweetDict['id'].append(str(idVal))
                    tweetDict['timestamp'].append(timestamp)
                    tweetDict['text'].append(text)
                    tweetDict['hashtag'].append(hashtags)
                    tweetDict['location'].append(location)
                    tweetDict['lang'].append(lang)
                    tweetDict['status'].append(status)
                    tweetDict['sentimentScore'].append(sentimentDict[idVal])

            except tweepy.TweepError as e:
                errorMessage = e.args[0][0]['message']
                errorCode = e.args[0][0]['code']
                print('Tweet ID {} had the following error: {} Error Code: {}'.format(idVal, errorMessage, errorCode))
                continue
        
    except KeyboardInterrupt:
        print('Next start: {}'.format((start + idx) * 100)) # Where to start the next time run the program. There may be duplicates included but duplicates are removed when all dataframes concatenated at the end.
        return pd.DataFrame(tweetDict)

    # Create the dataframe
    twitterDf = pd.DataFrame(tweetDict)
    
    # Write the dataframe to a csv
    directory = 'tweet_data/'
    files = os.listdir(directory)

    if len(files) == 0:
        fileName = directory + 'covidTweets_1_.csv'
    else:
      fileNum = str(int(files[-1].split('_')[1]) + 1)
      fileName = directory + 'covidTweets_' + fileNum + '_.csv'
    twitterDf.to_csv(fileName, index=False)
      
    
    # Print out the next Tweet id need to start at and the number that are left
    rateLimitRemaining = api.rate_limit_status()['resources']['statuses']['/statuses/lookup']['remaining']
    print('Rate Limit Remaining: {}'.format(rateLimitRemaining)) # Print the number of searches left
    print('Next start: {}'.format((start + numIterations) * 100))
    print('File {} created'.format(fileName))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
