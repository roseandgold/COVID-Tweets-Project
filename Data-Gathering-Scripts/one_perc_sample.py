'''
Script designed to take the cononets of a directory,
specifically searching for .csv files and then take a 1%
of each of those files and append them onto a final dataframe
which will in turn be writone to .csv

Ian Byrne, Laura Stagnaro
SIADS 591&592 Milestone I
Coronavirus Tweet Analysis Project
'''

import pandas as pd
import os


def one_perc_sample(df):
    '''takes a 1% sample of the provided dataframe'''

    data_sample = df.sample(frac=.01, random_state=52)
    return data_sample


def combined_samples():
    '''
    lists through all .csv files in ieee_data folder
    creating a dataframe then takes 1% sample of it
    then appends the sample to the final df
    '''

    directory = 'ieee_data/'
    final_sample = pd.DataFrame(columns=['tweet_id', 'sentiment_score'])

    for filename in os.listdir(directory):

        if filename.endswith(".csv"):
            day_sample = one_perc_sample(pd.read_csv(directory+filename, header=None,
                                                    names=['tweet_id', 'sentiment_score']))
            final_sample = final_sample.append(day_sample, ignore_index=True)
            print(filename)

    final_sample = final_sample.drop_duplicates(subset='tweet_id')
    return(final_sample)


def write_file(df):
    '''writes the final dataframe to csv'''

    # headers = ['tweet_id', 'sentiment_score']
    df.to_csv('sampled_tweetids.csv') # header=headers)


def main():
    '''Take samples, combine, and write files'''

    final_file = combined_samples()
    write_file(final_file)
    print('Done, daily samples taken. File length is {}'.format(len(final_file)))
    print(final_file.head())


if __name__ == "__main__":
    main()
