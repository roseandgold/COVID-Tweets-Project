'''
Transforms the Johns Hopkins COVID time series data from wide format to long
format and and aggregates the confirmed number of cases by country for each day.

Keyword arguments:
covidFile -- the filepath for the Johns Hopkins time series data

Outputs a CSV file with date, country, number of confirmed cases.

Laura Stagnaro, Ian Byrne
SIADS 591 & 592 Milestone I
Coronavirus Tweet Analysis Project
'''

import pandas as pd
import sys

def main(covidFile):
    
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
    covid = covid.groupby(['Date', 'Country']).agg({'Confirmed': sum}).reset_index()

    # Write the dataframe to a csv
    covid.to_csv('covidCountsCountryDay.csv', index=False)
    print('covidCountsCountryDay.csv created')
    print(covid.head())

if __name__ == "__main__":
    main(sys.argv[1])