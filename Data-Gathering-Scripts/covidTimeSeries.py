'''
Transforms the Johns Hopkins COVID time series data from wide format to long
format merges this data with the Tweet sentiment scores and calculates additional
information from the data.

Keyword arguments:
covidFile -- the filepath for the Johns Hopkins time series data
allTweetsFile -- the filepath for all the Tweets. This is needed to get the sentiment scores.

Output:
covidTimeSeries.csv -- a csv file with date, number of confirmed cases,
    number of new cases, 7 day rolling average number of cases,  min-max scaled
    7 day rolling average number of cases, average sentiment score, 
    7 day rolling average sentiment score, min-max scaled 7 day rolling average
    sentiment score.

Laura Stagnaro, Ian Byrne
SIADS 591 & 592 Milestone I
Coronavirus Tweet Analysis Project
'''

import pandas as pd
import sys
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def main(covidFile, allTweetsFile):
    
    # Get the file
    covid = pd.read_csv(covidFile)

    # Get the names of the countries to make the column names
    columns = list(covid['Country/Region'])

    # Transpose the dataframe
    covid = covid.transpose()

    # Make the countries the column names, remove the rows don't need, and reindex the dataframe
    covid.columns = columns
    covid = covid[4:].reset_index()

    # Rename the index column to date
    covid.rename(columns={'index':'Date'}, inplace=True)

    # Put the data in long form
    covid = covid.melt(id_vars = ['Date'], ignore_index=True)

    # Rename the columns
    covid.rename(columns={'variable': 'Country', 'value': 'Confirmed'}, inplace=True)

    # Change the date to datetime object to change date format in csv
    covid['Date'] = pd.to_datetime(covid['Date'])

    # Groupby date to get the total number of covid cases per day
    covid = covid.groupby('Date').agg({'Confirmed':sum}).reset_index()

    # Get the total number of new cases each day
    covid['New Cases'] = covid['Confirmed'].diff()

    # Get the 7 day rolling average for new cases
    covid['New Cases 7 Day Rolling Average'] = covid['New Cases'].rolling(window=7).mean().round()

    # Get the min max scale for rolling average
    avgConfirmedCases = covid['New Cases 7 Day Rolling Average'].values.reshape(-1,1)
    avgConfirmedCasesScaled = MinMaxScaler().fit_transform(avgConfirmedCases)
    covid['New Cases 7 Day Rolling Average (min-max scaled'] = avgConfirmedCasesScaled

    # Get the sentiment score
    sentiment = pd.read_csv(allTweetsFile, usecols = ['timestamp', 'sentimentScore'])
    
    # Create a date column and filter down to date and sentiment score columns
    sentiment['Date'] = pd.to_datetime(sentiment['timestamp']).dt.date
    sentiment['Date'] = pd.to_datetime(sentiment['Date'])
    sentiment = sentiment[['Date', 'sentimentScore']]

    # Calculate the average sentiment score per day
    sentiment = sentiment.groupby('Date').agg({'sentimentScore': np.mean}).reset_index()

    # Calculate the 7 day rolling average sentiment score
    sentiment['Sentiment 7 Day Rolling Average'] = sentiment['sentimentScore'].rolling(window=7).mean()

    # Calculate 7 day rolling average sentiment min max scaled
    avgSentiment = sentiment['Sentiment 7 Day Rolling Average'].values.reshape(-1,1)
    avgSentimentScaled = MinMaxScaler().fit_transform(avgSentiment)
    sentiment['Sentiment 7 Day Rolling Average (min-max scaled'] = avgSentimentScaled

    # Merge the dataframes on date to add the sentiment score
    covid = covid.merge(sentiment, how = 'outer', on='Date')

    # Rename columns
    covid.rename(columns = {'sentimentScore': 'Average Sentiment Score'}, inplace=True)

    # Write the dataframe to a csv
    covid.to_csv('covidTimeSeries.csv', index=False)
    print('covidTimeSeries.csv created')
    print(covid.head())
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])