# COVID_Project

SIADS 591/592 Milestone Project
Authors: Laura Stagnaro and Ian Byrne

## Data Sources Used
- [John Hopkins Global COVID-19 Time Series](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)
- [IEEE-Datapot](https://ieee-dataport.org/open-access/coronavirus-covid-19-tweets-dataset)
- [Twitter API](www.twitter.com)

## Data Manipulation Stages
- Manually downloaded the Twitter ID CSV files and Zip files
- Grab a one percent sample for each day (each CSV represented one day of Tweets) one_perc_sample.py
- Retrieve the full tweets from the Twitter API with twitterAPIScript.py
- Combine all of the tweet data into one CSV combineTweetCSVs.py
- Grab the bi-grams for each tweet tweetTokenizer.py
- Tokenize each tweet to get individual words tweetTokenizerSingleWord.py
- Daily covid case counts by country covidCountsCountryDay.py
- Total cases per day covidTimeSeries.py

## Analysis

