'''
Processes the raw Tweets in allTweets.csv by tokenizing, 
lemmatizing, and making them into single words.

Returns tokenizedTweetsSingleWord.csv which contains the Tweet id number, words, and date.

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


def tokenizeLemmatizeTweets(tweet):
    '''Cleans the raw Tweets and produces 3 word ngrams of the Tweets.
    
    Keyword argument:
    tweet -- the Tweet to be processed
    
    Return:
    ngramList -- a list of three word ngrams

    ''' 
    # Create the tokenizer and lemmatizer
    tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
    lemmatizer = WordNetLemmatizer()

    # Tokenize the Tweet
    tokenized = tokenizer.tokenize(tweet)
    
    # Some of the below code was found here: https://www.youtube.com/watch?v=7N_2OsLXFlA&list=PLmcBskOCOOFW1SNrz6_yzCEKGvh65wYb9&index=19
    # Create variables that store the punctuation and stopwords to be removed
    punctuation = list(string.punctuation)
    swords = stopwords.words('english') + punctuation + ['rt', 'via', '...', 'u', 'ur', 'r', 'covid', 'coronavirus', 'covid19']

    # Create a list of lemmatized words, remove punctuation, stopwords and numbers
    tokenList = [lemmatizer.lemmatize(word) for word in tokenized if word not in swords and not word.isdigit()]
    
    return tokenList

def main():
    
    # Get the file
    allTweets = pd.read_csv('allTweets.csv')
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
    allTweets = allTweets[['id', 'date', 'tokenized']]
    allTweets = allTweets.explode('tokenized')

    # Sort the dataframe by date
    allTweets = allTweets.sort_values('date')
    
    # Create the csv
    allTweets.to_csv('tokenizedTweetsSingleWord.csv', index = False)
    
    print('tokenizedTweetsSingleWord.csv created')
    print(allTweets.head())
    
if __name__ == "__main__":
    main()