'''Script to loop through the directory with all
of the covid case data by country and combine it
into the a single .csv
'''

import os
import pandas as pd


def process_cases(df):
    '''Drop updates, FIPS, and Admin2 cols and
    sets the index to the date of the .csv based
    on the Last_Update col.
    '''

    # grab date only from datetime
    df['Last_Update'] = pd.to_datetime(df['Last_Update'])
    df['Date'] = df['Last_Update'].dt.date

    cols_to_drop = ['FIPS', 'Admin2', 'Last_Update']
    clean_df = df.drop(columns=cols_to_drop)

    clean_df.set_index('Date', inplace=True)

    return clean_df


def combined_samples():
    '''
    lists through all .csv files in case_data folder
    to create one file with all dates.
    '''

    directory = 'case_data/'
    combined_cases = pd.DataFrame(columns=[
        'FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update',
        'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active',
        'Combined_Key', 'Incidence_Rate', 'Case-Fatality_Ratio'
    ])

    for filename in os.listdir(directory):

        if filename.endswith(".csv"):
            day = pd.read_csv(directory+filename)

            combined_cases = combined_cases.append(day, ignore_index=True)
            print(filename, len(day), len(combined_cases))

    print(len(combined_cases))
    return combined_cases


def write_file(df):
    '''writes the final dataframe to csv'''

    # headers = ['tweet_id', 'sentiment_score']
    df.to_csv('covid_case_data.csv', chunksize=25000)


def main():
    '''Combines cases, processes, then writes to file'''

    allcases = combined_samples()
    print('all cases combined')

    final = process_cases(allcases)
    print('cases processed and date set as index')
    print('writing file...')
    write_file(final)
    print('Done')


if __name__ == "__main__":
    main()
