'''
Transforms the Johns Hopkins COVID time series data from wide format to long
format and and aggregates the confirmed number of cases by country for each day.

Keyword arguments:
covidFile -- the filepath for the Johns Hopkins time series data

Outputs a CSV file with date, country, number of confirmed cases and 
COVID phase label.

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

    # Filter down to the necessary dates
    covid = covid[(covid['Date'] >= '2020-03-01') & (covid['Date'] <= '2020-09-01')]
    covid['Date'] = covid['Date'].dt.date

    # Groupby date to get the total number of covid cases per day
    covid = covid.groupby(['Date', 'Country']).agg({'Confirmed': sum}).reset_index()

    # Add what covid phase the count falls into
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
    covid['covid phase'] = covid['Date'].map(phaseDict)

    # Write the dataframe to a csv
    covid.to_csv('covidCountsCountryDay.csv', index=False)
    print('covidCountsCountryDay.csv created')
    print(covid.head())

if __name__ == "__main__":
    main(sys.argv[1])