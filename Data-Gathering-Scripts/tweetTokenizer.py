'''
Processes the raw Tweets in a csv by tokenizing, 
lemmatizing, and making them into bi-grams.

Keyword Arguments:
tweetData -- the file which contains all the Tweets

Output: 
tokenizedTweets.csv  -- contains the count for each bi-gram per day.

If you have not installed the below packages they must be installed
    nltk.download('stopwords')
    nltk.download('wordnet')

Laura Stagnaro, Ian Byrne
SIADS 591 & 592 Milestone I
Coronavirus Tweet Analysis Project
'''

import pandas as pd
import string
import numpy as np
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.util import ngrams
import sys


def tokenizeLemmatizeTweets(tweet):
    '''Cleans the raw Tweets and produces bi-grams of the Tweets.
    
    Keyword argument:
    tweet -- the Tweet to be processed
    
    Return:
    ngramList -- a list of bi-grams

    ''' 
    # Create the tokenizer and lemmatizer
    tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
    lemmatizer = WordNetLemmatizer()

    # Tokenize the Tweet
    tokenized = tokenizer.tokenize(tweet)
    
    # Some of the below code was found here: https://www.youtube.com/watch?v=7N_2OsLXFlA&list=PLmcBskOCOOFW1SNrz6_yzCEKGvh65wYb9&index=19
    # Create variables that store the punctuation and stopwords to be removed
    punctuation = list(string.punctuation)
    swords = stopwords.words('english') + punctuation + ['rt', 'via', '...', '..', 'u', 'ur', 'r', 'n']

    # Create a list of lemmatized words, remove punctuation, stopwords and numbers
    tokenList = [lemmatizer.lemmatize(word) for word in tokenized if lemmatizer.lemmatize(word) not in swords and not word.isdigit()]
    ngramList = [ngram for ngram in ngrams(tokenList, 2)]
    
    return ngramList

def main(tweetFile):
    
    # Get the file
    allTweets = pd.read_csv(tweetFile, usecols = ['id','timestamp', 'text'])
    allTweets = allTweets.drop_duplicates()
    
    # Change the timestamp to datetime and create a date column
    allTweets['timestamp'] = pd.to_datetime(allTweets['timestamp'])
    allTweets['date']  = allTweets['timestamp'].dt.date
    
    # Change all tweets to lowercase and remove any non-ASCII characters
    # Found code from: https://stackoverflow.com/questions/36340627/remove-non-ascii-characters-from-pandas-column
    allTweets['text'] = allTweets['text'].str.lower().str.encode('ascii', 'ignore').str.decode('ascii')
    
    # Remove all links and multiple hashes for one hashtagged word
    allTweets = allTweets.replace({'text': {r"http\S+": "", '#{1,}': ""}}, regex=True)
    
    # Add the tokenized words column
    allTweets['tokenized'] = allTweets['text'].apply(tokenizeLemmatizeTweets)
    
    # Reduce the dataframe and explode the tokens to their own rows
    allTweets = allTweets[['id','date', 'tokenized']]
    allTweets = allTweets.explode('tokenized')
    
    # Groupby the date and ngram to get the counts
    allTweets = allTweets.groupby(['date', 'tokenized']).count().reset_index().sort_values('date')
    allTweets.rename(columns = {'id': 'counts'}, inplace = True)

    # Add what covid phase the bigram fell into
    # Create a list of dates for each phase
    phase1Dates = list(pd.date_range('2020-03-01', '2020-04-07', freq = 'D'))
    phase2Dates = list(pd.date_range('2020-04-08', '2020-05-12', freq = 'D'))
    phase3Dates = list(pd.date_range('2020-05-13', '2020-07-28', freq = 'D'))
    phase4Dates = list(pd.date_range('2020-07-29', '2020-09-01', freq= 'D'))

    # Put the list of dates into one list
    allDates = phase1Dates + phase2Dates + phase3Dates + phase4Dates

    # Create lists with the phase labels
    phase1 = ['phase 1'] * len(phase1Dates)
    phase2 = ['phase 2'] * len(phase2Dates)
    phase3 = ['phase 3'] * len(phase3Dates)
    phase4 = ['phase 4'] * len(phase4Dates)

    # Put the list of labels into one list
    allPhases = phase1 + phase2 + phase3 + phase4

    # Create a dictionary with the phases and dates
    phaseDict = dict(zip(allDates, allPhases))

    # Create the phase label column
    allTweets['covid phase'] = allTweets['date'].map(phaseDict)
    
    # Create the csv
    allTweets.to_csv('tokenizedTweets.csv', index = False)
    
    print('tokenizedTweets.csv created')
    print(allTweets.head())
    
if __name__ == "__main__":
    main(sys.argv[1])