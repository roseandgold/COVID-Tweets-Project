'''
Combines all CSVs which contain hydrated Twitter data.

Requires a folder named "tweet_data" which contains the CSVs to be combined.
Outputs a file titled "allTweets.csv".

Laura Stagnaro, Ian Byrne
SIADS 591 & 592 Milestone I
Coronavirus Tweet Analysis Project

'''
import pandas as pd
import os

def main():
    '''Concatenate all CSVs with Twitter information.'''
    
    directory = 'tweet_data/'
    twitterDf = pd.DataFrame(columns = ['id', 'timestamp', 'text', 'hashtag', 'location', 'lang', 'sentimentScore', 'status'])
    
    for filename in os.listdir(directory):
        
        if filename.endswith(".csv"):
            df = pd.read_csv(directory + filename)
            twitterDf = twitterDf.append(df, ignore_index=True)
            print(directory + filename, len(df))
        
    twitterDf = twitterDf.drop_duplicates(subset=['id']) # Remove any duplicate Tweets
    twitterDf.to_csv('allTweets.csv', index=False) # Create the csv file
    print('{} created with {} Tweets'.format('allTweets.csv', len(twitterDf)))

if __name__ == "__main__":
    main()
