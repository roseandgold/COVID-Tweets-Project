'''Package of functions designed to be imported into a jupyter notebook
and generate one liner graphs'''

import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def read_day_counts():
    """Reads in the daily word counts file and cleans it:
    - drops the unnamed:0 column
    - sets the date to datetime
    """

    df = pd.read_csv('allTokenizedTweetsSingleWord.csv')

    # df.rename(columns={'date': 'string_date'}, inplace=True)
    df['string_date'] = df['date']
    df['date'] = pd.to_datetime(df['date'])
    # df.set_index('date', inplace=True)
    reduced = df[df['counts'] > 20]

    return reduced


def get_dates(df):
    '''Retrieves the dates in string form for drop down'''

    dates = list(df['string_date'].unique())
    dates.sort()

    return dates


def select_date(df, date):
    """Filters dataframe down to specific date
    - used within the daily_top10_barchart() function"""

    df_day = df.loc[df['date'] == date]

    return df_day


def daily_top10_barchart(df, date):
    '''Displays the top 10 words mentioned on the date selected'''

    # narrow down to correct date df
    data = select_date(df, date)

    # retrieve the top 10 words
    data2 = data.nlargest(10, 'counts')

    # create barchart TODO: add better axis labels and themes
    barchart = px.bar(data_frame=data2,
                      x='tokenized',
                      y='counts',
                      color='tokenized',
                      opacity=0.9,
                      orientation='v',
                      barmode='relative')

    # display barchart
    pio.show(barchart)


def get_top100(df):

    # get top 100 most mentioned words
    grouped = df.groupby('tokenized', as_index=False).sum()
    grouped.sort_values(by='counts', ascending=False, inplace=True)
    top100 = grouped[:100]

    # check
    top = df[df.tokenized.isin(top100['tokenized'])]

    # take top 100 and add a cumulative sum columns
    top1 = top.groupby(['tokenized', 'date']).sum()
    top1['cumsum'] = top1.groupby(level=0).cumsum()
    top1.reset_index(inplace=True)

    return top1


def words_linechart_one():

    # create word data frames
    df = read_day_counts()
    main_words = ['pandemic', 'virus', 'lockdown']
    top_words = get_top100(df)
    top_words_cum = top_words[top_words['tokenized'].isin(main_words)]

    covid = pd.read_csv('covidTimeSeries.csv')

    lockdown = top_words_cum[top_words_cum['tokenized'] == 'lockdown']
    pandemic = top_words_cum[top_words_cum['tokenized'] == 'pandemic']
    virus = top_words_cum[top_words_cum['tokenized'] == 'virus']

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    # Lockdown mentions
    fig.add_trace(
        go.Scatter(x=lockdown['date'],
                   y=lockdown['cumsum'],
                   name="Lockdown mentions"),
        secondary_y=False,
    )

    # Pandemic Mentions
    fig.add_trace(
        go.Scatter(x=pandemic['date'],
                   y=pandemic['cumsum'],
                   name="Pandemic mentions"),
        secondary_y=False,
    )

    # Virus Mentions
    fig.add_trace(
        go.Scatter(x=virus['date'], y=virus['cumsum'], name="Virus mentions"),
        secondary_y=False,
    )

    # Covid cases
    fig.add_trace(
        go.Scatter(x=covid['Date'],
                   y=covid['Confirmed'],
                   name="Total Covid Cases",
                   line=dict(color='black', width=4, dash='dash')),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text=
        "'Lockdown', 'Pandemic', and 'Virus' mentions with Total Cases")

    # Set x-axis title
    # fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Mention Counts</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>COVID Case totals</b>", secondary_y=True)

    fig.show()


def get_top10_words(df):
    '''grabs the top 5 words over time during the pandemic'''

    data = df.groupby('tokenized', as_index=False).sum()
    final = data.nlargest(10, 'counts')

    print(final['tokenized'].unique())
    return final


def words_linechart_two():

    # create word data frames
    df = read_day_counts()
    main_words = ['pandemic', 'people', 'case', 'trump', 'death', 'mask']
    top_words = get_top100(df)
    top_words_cum = top_words[top_words['tokenized'].isin(main_words)]

    covid = pd.read_csv('covidTimeSeries.csv')

    pandemic = top_words_cum[top_words_cum['tokenized'] == 'pandemic']
    people = top_words_cum[top_words_cum['tokenized'] == 'people']
    case = top_words_cum[top_words_cum['tokenized'] == 'case']
    trump = top_words_cum[top_words_cum['tokenized'] == 'trump']
    death = top_words_cum[top_words_cum['tokenized'] == 'death']
    mask = top_words_cum[top_words_cum['tokenized'] == 'mask']

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    # Pandemic mentions
    fig.add_trace(
        go.Scatter(x=pandemic['date'],
                   y=pandemic['cumsum'],
                   name="Pandemic mentions (1)"),
        secondary_y=False,
    )

    # People Mentions
    fig.add_trace(
        go.Scatter(x=people['date'],
                   y=people['cumsum'],
                   name="People mentions (3)"),
        secondary_y=False,
    )

    # Case Mentions
    fig.add_trace(
        go.Scatter(x=case['date'], y=case['cumsum'], name="Case mentions (5)"),
        secondary_y=False,
    )

    # Trump Mentions
    fig.add_trace(
        go.Scatter(x=trump['date'],
                   y=trump['cumsum'],
                   name="Trump mentions (6)"),
        secondary_y=False,
    )

    # Death Mentions
    fig.add_trace(
        go.Scatter(x=death['date'],
                   y=death['cumsum'],
                   name="Death mentions (7)"),
        secondary_y=False,
    )
    # Mask Mentions
    fig.add_trace(
        go.Scatter(x=mask['date'], y=mask['cumsum'], name="Mask mentions (8)"),
        secondary_y=False,
    )

    # Covid cases
    fig.add_trace(
        go.Scatter(x=covid['Date'],
                   y=covid['Confirmed'],
                   name="Total Covid Cases",
                   line=dict(color='black', width=4, dash='dash')),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(title_text="Most meaningful words and Covid case totals")

    # Set x-axis title
    # fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Mention Counts</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>COVID Case totals</b>", secondary_y=True)

    fig.show()
