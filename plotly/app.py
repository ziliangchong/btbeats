from _plotly_future_ import v4_subplots
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from textwrap import dedent
import base64

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
server = app.server

app.config['suppress_callback_exceptions']=True #to enable callbacks within callbacks

app.title = 'BT BEATS' #change the display in the browser tab

def encode_image(image_file): #function to encode image, otherwise wont display
    encoded = base64.b64encode(open(image_file,'rb').read()) #call base64, b64encode, open image file, read binary
    return 'data:image/jpg;base64,{}'.format(encoded.decode()) #return with the string that allows python to read, with the decoded encoded image

#read in data to plot
bt_df = pd.read_csv('./datasets/bt/bt_abridged.csv')
bt_df['date'] = pd.to_datetime(bt_df['date'])

quart_df = pd.read_csv('./datasets/economic-data/quart.csv')
quart_df.drop('Unnamed: 0', axis=1, inplace=True)
quart_df['date'] = pd.to_datetime(quart_df['date'])

month_df = pd.read_csv('./datasets/economic-data/month.csv')
month_df.drop('Unnamed: 0', axis=1, inplace=True)
month_df['date'] = pd.to_datetime(month_df['date'])

indicators_quarter = ['GDP growth', 'Composite', 'Industrial production', 'Merchandise trade', 'Retail sales']
columns_quarter = [col for col in quart_df.drop('date', axis=1).columns] #generate labels for the BEATS index drop down
options_index_quarter = [{'label':col[0], 'value':col[1]} for col in list(zip(indicators_quarter, columns_quarter))]

indicators_month = ['Industrial production', 'Merchandise trade', 'Retail sales']
columns_month = [col for col in month_df.drop('date', axis=1).columns] #generate labels for the BEATS index drop down
options_index_month = [{'label':col[0], 'value':col[1]} for col in list(zip(indicators_month, columns_month))]

string_years = ['2014', '2015', '2016', '2017', '2018', '2019'] #generate labels for topics year
options_topic_year = [{'label': year, 'value': year} for year in string_years]

topic_quarter = [] #generate labels for topics quarter

for year in string_years:
    for i in range(4):
        topic_quarter.append(year + 'Q' + str(i+1)) #create list of quarters

topic_quarter.remove('2019Q4')  #remove this quarter as data doesnt exist for this quarter

options_topic_quarter = [{'label': quarter, 'value': quarter} for quarter in topic_quarter]

#master tab external_styles

master_tabs_styles = {
    'height': '44px'
}

master_tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

master_tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#047CAC',
    'color': 'white',
    'padding': '6px'
}

#markdowns
intro_text = '''
**The Business & Economic Activity Trends & Sentiment, or BEATS,**
is a brand new economic indicator that tracks the pulse of the economy through news articles from [The Business Times](https://www.businesstimes.com.sg),
Singapore's flagship business media outlet.
'''

BEATS_index_text = '''
Using natural language processing, a machine learning technique, every article in The Business Times is scored for a sentiment between 1 (most positive) and -1 (most negative).
The scores are then averaged out to form an index, reflecting real-time economic and business sentiment.
Compare the BEATS index to traditional economic indicators below.
'''

topics_text = '''
BEATS is able to discern topics and trends from articles across a particular period of time.
Choose a year or quarter to see the major themes of that period, as covered by The Business Times.
Each year is grouped into 10 topics while each quarter is segmented into five.
The larger the size of a word in a word cloud, the stronger its association to that topic.
'''

subject_analysis_text = '''
Pick a subject or company and enter it below to see how its sentiment score compares to the overall BEATS index.
Hovering over the graph brings up top positive and negative headlines of that period, if there are enough articles written on the subject in that quarter.
'''

acknowledgement_text = '''
**Under the hood:**  \n
- [VADER (Valence Aware Dictionary and sEntiment Reasoner)](https://github.com/cjhutto/vaderSentiment) for scoring the articles
- [Loughran-McDonald list](https://sraf.nd.edu/textual-analysis/resources/#LM%20Sentiment%20Word%20Lists) of financial terms to augment VADER
- [Latent Dirichlet Allocation](https://scikit-learn.org/stable/modules/decomposition.html#latentdirichletallocation) for topic modelling
- [Dash](https://dash.plot.ly/?_ga=2.184356774.1848931800.1567237470-996460834.1566799314) for building this dashboard
- All news articles used are courtesy of [Singapore Press Holdings](https://www.sph.com.sg/)
- [Similar](https://www.mti.gov.sg/-/media/MTI/Legislation/Public-Consultations/2016/Economic-Sentiments-in-Singapore/ba_2q16.pdf) [research](https://www.mti.gov.sg/-/media/MTI/Legislation/Public-Consultations/2018/Recent-Trends-in-Singapore-News-Economic-Sentiments/ba_1q18.pdf) done by Singapore's [Ministry of Trade and Industry](https://www.mti.gov.sg)
'''

contact_text = '''
**Contact me:**  \n

'''

#app layout

app.layout = html.Div([
    html.H1('BT BEATS', style={'color':'white', 'background-color':'#047CAC', 'textAlign':'center'}),
    html.Div([
        dcc.Markdown(children=intro_text)
    ], style={'width':'70%', 'display':'inline-block'}),
    html.Div([
        html.Div([
            dcc.Markdown(children='**Powered by:**')
        ]),
        html.A([
            html.Img(src=encode_image("./images/icons/bt.jpg"), width=300)
        ], href='https://www.businesstimes.com.sg')
    ], style={'display':'inline-block', 'paddingLeft':'20px', 'borderLeft': '1px solid #E1E1E1'}),
    html.Hr(),
    html.Div([
        dcc.Tabs(id="master-tabs", value='tab-index', children=[
            dcc.Tab(label='BEATS Index', value='tab-index', style=master_tab_style, selected_style=master_tab_selected_style),
            dcc.Tab(label='Trending Topics', value='tab-topic', style=master_tab_style, selected_style=master_tab_selected_style),
            dcc.Tab(label='Subject Analysis', value='tab-subject', style=master_tab_style, selected_style=master_tab_selected_style)
    ], style=master_tabs_styles),
    html.Div(id='master-tabs-content')
    ]),
    html.Hr(),
    html.Div([
        dcc.Markdown(children=acknowledgement_text)
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'70%', 'borderRight': '1px solid #E1E1E1'}),
    html.Div([
    html.Div([
    dcc.Markdown(children=contact_text)
    ]),
    html.Div([
        html.Div([
            html.Img(src=encode_image("./images/icons/email.jpg"), width=20, style={'paddingRight':'5px'})
        ], style={'display':'inline-block', 'verticalAlign':'middle'}),
        html.Div([
            dcc.Markdown(children='zi.liang.chong@gmail.com')
        ], style={'display':'inline-block', 'paddingRight':'20px'}),
        ]),
        html.Div([
            html.Div([
                html.Img(src=encode_image("./images/icons/linkedin.jpg"), width=20, style={'paddingRight':'5px'})
            ], style={'display':'inline-block', 'verticalAlign':'middle'}),
            html.Div([
                dcc.Markdown(children='[linkedin.com/in/zi-liang-chong](https://www.linkedin.com/in/zi-liang-chong/)')
            ], style={'display':'inline-block', 'paddingRight':'20px'}),
        ]),
        html.Div([
            html.Div([
                html.Img(src=encode_image("./images/icons/github.jpg"), width=20, style={'paddingRight':'5px'})
            ], style={'display':'inline-block', 'verticalAlign':'middle'}),
            html.Div([
                dcc.Markdown(children='[github.com/ziliangchong](https://github.com/ziliangchong)')
            ], style={'display':'inline-block'})
        ])
    ], style={'paddingLeft':'30px', 'display':'inline-block'})
], style={'paddingLeft':'5px', 'paddingRight':'5px'})

@app.callback(Output('master-tabs-content', 'children'),
              [Input('master-tabs', 'value')])
def render_master_content(tab):
    if tab == 'tab-index':
        return html.Div([
            html.H2('BEATS Index', style={'textAlign': 'center'}),
            html.Div([
            dcc.Markdown(children=BEATS_index_text)
            ]),
            html.Div([
            dcc.Tabs(id="BEATS-tabs", value='quarterly-data', children=[
                dcc.Tab(label='Quarterly data', value='quarterly-data'),
                dcc.Tab(label='Monthly data', value='monthly-data'),
            ]),
            html.Div(id='BEATS-tabs-content')
            ])
        ])

    elif tab == 'tab-topic':
        return html.Div([
            html.H2('Trending Topics', style={'textAlign': 'center'}),
            html.Div([
            dcc.Markdown(children=topics_text)
            ]),
            html.Div([
            dcc.Tabs(id="topics-tabs", value='yearly-topics', children=[
                dcc.Tab(label='Yearly topics', value='yearly-topics'),
                dcc.Tab(label='Quarterly topics', value='quarterly-topics'),
            ]),
            html.Div(id='topics-tabs-content')
            ])
        ])

    elif tab == 'tab-subject':
        return html.Div([
            html.H2('Subject Analysis', style={'textAlign': 'center'}),
            html.Div([
            dcc.Markdown(children=subject_analysis_text)
            ]),
            html.Div([
                html.H3('Select subject:'),
                dcc.Input(
                    id='my_subject',
                    value='DBS',#default value
                )
            ], style={'display':'inline-block', 'verticalAlign':'bottom'}),
            html.Div([
                html.Button(
                    id='submit-button-subject',
                    n_clicks=0,
                    children='Submit',
                    style={'fontSize':14, 'marginLeft':'10px'}
                ),
            ], style={'display':'inline-block'}),
            dcc.Graph(
                id='subject_graph'
            ),
            html.Div([
            dcc.Markdown(id='hover-data-pos')
            ], style={'width':'45%', 'paddingLeft':'30px', 'display':'inline-block'}),
            html.Div([
            dcc.Markdown(id='hover-data-neg')
            ], style={'width':'45%', 'paddingLeft':'1px', 'display':'inline-block'})
        ])

@app.callback(Output('BEATS-tabs-content', 'children'), #callback for BEATS index
              [Input('BEATS-tabs', 'value')])
def render_content_beats(tab):
    if tab == 'quarterly-data':

        return html.Div([
            html.Div([
                html.H3('Select lag:', style={'paddingRight':'30px'}),
                dcc.Dropdown(
                    id='my_lag_quarter',
                    options=[{'label': 'No - plot BEATS Index at original timestamp', 'value': 0},
                            {'label': 'Yes - lag BEATS Index by one quarter so 2014Q1 sentiment is plotted at 2014Q2, etc', 'value': 1}],
                    value=0 #default value
                ),
                html.H3('Select indicators:', style={'paddingRight':'30px'}),
                dcc.Dropdown(
                    id='my_indicators_quarter',
                    options=options_index_quarter,
                    value=['gdp_growth'],#default value
                    multi=True
                )
            ], style={'display':'inline-block', 'verticalAlign':'bottom', 'width':'50%'}),
            dcc.Graph(
                id='BEATS-quarterly-graph'
            )
        ])

    elif tab == 'monthly-data':

        return html.Div([
            html.Div([
                html.H3('Select lag:', style={'paddingRight':'30px'}),
                dcc.Dropdown(
                    id='my_lag_month',
                    options=[{'label': 'No - plot BEATS Index at original timestamp', 'value': 0},
                            {'label': 'Yes - lag BEATS Index by one month so 2014 Jan sentiment is plotted at 2014 Feb, etc', 'value': 1}],
                    value=0 #default value
                ),
                html.H3('Select indicators:', style={'paddingRight':'30px'}),
                dcc.Dropdown(
                    id='my_indicators_month',
                    options=options_index_month,
                    value=['industrial'],#default value
                    multi=True
                )
            ], style={'display':'inline-block', 'verticalAlign':'bottom', 'width':'50%'}),
            dcc.Graph(
                id='BEATS-monthly-graph'
            )
        ])


@app.callback( #callback for BEATS index quarterly graph
    Output('BEATS-quarterly-graph', 'figure'),
    [Input('my_lag_quarter', 'value'),
    Input('my_indicators_quarter', 'value')])
def update_graph_index_quarter(lag_value, indicators_value):

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=bt_df.groupby(bt_df.date.dt.to_period('Q'))['compound'].mean().index.to_timestamp().shift(lag_value),
                    y=bt_df.groupby(bt_df.date.dt.to_period('Q'))['compound'].mean().values,
                    name="Beats"),
        secondary_y=False,
    ) #groupby period then take mean of compound score, plot x is time, y is mean compound score

    labels = []
    for value in indicators_value:
        for pair in list(zip(indicators_quarter, columns_quarter)):
            if value == pair[1]:
                labels.append(pair[0])

    for i, col in enumerate(indicators_value):
        fig.add_trace(
            go.Scatter(x=quart_df['date'],
                        y=quart_df[col],
                        name=labels[i]),
            secondary_y=True,
        )

    # Add figure title
    fig.layout.update(
        title_text="BEATS index and quarterly indicators"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="BEATS", secondary_y=False)
    fig.update_yaxes(title_text="Economic indicators (% growth)", secondary_y=True)

    return fig

@app.callback( #callback for BEATS index monthly graph
    Output('BEATS-monthly-graph', 'figure'),
    [Input('my_lag_month', 'value'),
    Input('my_indicators_month', 'value')])
def update_graph_index_month(lag_value, indicators_value):

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    if lag_value == 1: #this more complicated workaround is needed instead of simply using .shift because groupby month gives no self frequency, unlike groupby quarter, leading to complications with shifting
        fig.add_trace(
            go.Scatter(x=bt_df.groupby(bt_df.date.dt.to_period('m'))['compound'].mean().index.to_timestamp().shift(lag_value, freq='m').shift(lag_value, freq='d'),
                        y=bt_df.groupby(bt_df.date.dt.to_period('m'))['compound'].mean().values,
                        name="Beats"),
            secondary_y=False,
        )
    else:
        fig.add_trace(
            go.Scatter(x=bt_df.groupby(bt_df.date.dt.to_period('m'))['compound'].mean().index.to_timestamp(),
                        y=bt_df.groupby(bt_df.date.dt.to_period('m'))['compound'].mean().values,
                        name="Beats"),
            secondary_y=False,
        ) #groupby period then take mean of compound score, plot x is time, y is mean compound score

    labels = []
    for value in indicators_value:
        for pair in list(zip(indicators_month, columns_month)):
            if value == pair[1]:
                labels.append(pair[0])

    for i, col in enumerate(indicators_value):
        fig.add_trace(
            go.Scatter(x=month_df['date'],
                        y=month_df[col],
                        name=labels[i]),
            secondary_y=True,
        )

    # Add figure title
    fig.layout.update(
        title_text="BEATS index and monthly indicators"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="BEATS", secondary_y=False)
    fig.update_yaxes(title_text="Economic indicators (% growth)", secondary_y=True)

    return fig

@app.callback(Output('topics-tabs-content', 'children'), #callback for topics
              [Input('topics-tabs', 'value')])
def render_content_beats(tab):
    if tab == 'yearly-topics':

        return html.Div([
            html.Div([
                html.H3('Select year:', style={'paddingRight':'30px'}),
                dcc.Dropdown(
                    id='my_topics_year',
                    options=options_topic_year,
                    value='2014'#default value
                )
            ], style={'display':'inline-block', 'verticalAlign':'bottom', 'paddingBottom':'30px', 'width':'20%'}),
            html.Div([ #five wordclouds in one div, for them to appear side by side
            html.Img(id='image-topic-year-0', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-year-1', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-year-2', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-year-3', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-year-4', width=250, style={'paddingRight':'20px'})
            ], style={'paddingLeft':'35px', 'paddingBottom':'30px'}), #pad so the first wordcloud not at the edge, padding bottom to give space between first and second row of wordclouds
            html.Div([ #five wordclouds in one div, for them to appear side by side, second line of wordclouds
            html.Img(id='image-topic-year-5', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-year-6', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-year-7', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-year-8', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-year-9', width=250, style={'paddingRight':'20px'})
            ], style={'paddingLeft':'35px'}) #pad so the first wordcloud not at the edge
        ])

    elif tab == 'quarterly-topics':

        return html.Div([
            html.Div([
                html.H3('Select quarter:', style={'paddingRight':'30px'}),
                dcc.Dropdown(
                    id='my_topics_quarter',
                    options=options_topic_quarter,
                    value='2014Q1'#default value
                )
            ], style={'display':'inline-block', 'verticalAlign':'bottom', 'paddingBottom':'30px', 'width':'20%'}),
            html.Div([ #five wordclouds in one div, for them to appear side by side
            html.Img(id='image-topic-quarter-0', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-quarter-1', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-quarter-2', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-quarter-3', width=250, style={'paddingRight':'20px'}),
            html.Img(id='image-topic-quarter-4', width=250, style={'paddingRight':'20px'})
            ], style={'paddingLeft':'35px', 'paddingBottom':'30px'}) #pad so the first wordcloud not at the edge, padding bottom to give space between first and second row of wordclouds
        ])

@app.callback( #callback for yearly topic 0
    Output('image-topic-year-0', 'src'),
    [Input('my_topics_year', 'value')])
def update_topic_year_0(year_value):

    return encode_image("./images/year_word_cloud/{}-topic-0.jpg".format(year_value))

@app.callback( #callback for yearly topic 1
    Output('image-topic-year-1', 'src'),
    [Input('my_topics_year', 'value')])
def update_topic_year_1(year_value):

    return encode_image("./images/year_word_cloud/{}-topic-1.jpg".format(year_value))

@app.callback( #callback for yearly topic 2
    Output('image-topic-year-2', 'src'),
    [Input('my_topics_year', 'value')])
def update_topic_year_2(year_value):

    return encode_image("./images/year_word_cloud/{}-topic-2.jpg".format(year_value))

@app.callback( #callback for yearly topic 3
    Output('image-topic-year-3', 'src'),
    [Input('my_topics_year', 'value')])
def update_topic_year_3(year_value):

    return encode_image("./images/year_word_cloud/{}-topic-3.jpg".format(year_value))

@app.callback( #callback for yearly topic 4
    Output('image-topic-year-4', 'src'),
    [Input('my_topics_year', 'value')])
def update_topic_year_4(year_value):

    return encode_image("./images/year_word_cloud/{}-topic-4.jpg".format(year_value))

@app.callback( #callback for yearly topic 5
    Output('image-topic-year-5', 'src'),
    [Input('my_topics_year', 'value')])
def update_topic_year_5(year_value):

    return encode_image("./images/year_word_cloud/{}-topic-5.jpg".format(year_value))

@app.callback( #callback for yearly topic 6
    Output('image-topic-year-6', 'src'),
    [Input('my_topics_year', 'value')])
def update_topic_year_6(year_value):

    return encode_image("./images/year_word_cloud/{}-topic-6.jpg".format(year_value))

@app.callback( #callback for yearly topic 7
    Output('image-topic-year-7', 'src'),
    [Input('my_topics_year', 'value')])
def update_topic_year_7(year_value):

    return encode_image("./images/year_word_cloud/{}-topic-7.jpg".format(year_value))

@app.callback( #callback for yearly topic 8
    Output('image-topic-year-8', 'src'),
    [Input('my_topics_year', 'value')])
def update_topic_year_8(year_value):

    return encode_image("./images/year_word_cloud/{}-topic-8.jpg".format(year_value))

@app.callback( #callback for yearly topic 9
    Output('image-topic-year-9', 'src'),
    [Input('my_topics_year', 'value')])
def update_topic_year_9(year_value):

    return encode_image("./images/year_word_cloud/{}-topic-9.jpg".format(year_value))

@app.callback( #callback for quarterly topic 0
    Output('image-topic-quarter-0', 'src'),
    [Input('my_topics_quarter', 'value')])
def update_topic_year_0(quarter_value):

    return encode_image("./images/quarter_word_cloud/{}-topic-0.jpg".format(quarter_value))

@app.callback( #callback for quarterly topic 1
    Output('image-topic-quarter-1', 'src'),
    [Input('my_topics_quarter', 'value')])
def update_topic_year_1(quarter_value):

    return encode_image("./images/quarter_word_cloud/{}-topic-1.jpg".format(quarter_value))

@app.callback( #callback for quarterly topic 2
    Output('image-topic-quarter-2', 'src'),
    [Input('my_topics_quarter', 'value')])
def update_topic_year_2(quarter_value):

    return encode_image("./images/quarter_word_cloud/{}-topic-2.jpg".format(quarter_value))

@app.callback( #callback for quarterly topic 3
    Output('image-topic-quarter-3', 'src'),
    [Input('my_topics_quarter', 'value')])
def update_topic_year_3(quarter_value):

    return encode_image("./images/quarter_word_cloud/{}-topic-3.jpg".format(quarter_value))

@app.callback( #callback for quarterly topic 4
    Output('image-topic-quarter-4', 'src'),
    [Input('my_topics_quarter', 'value')])
def update_topic_year_4(quarter_value):

    return encode_image("./images/quarter_word_cloud/{}-topic-4.jpg".format(quarter_value))

@app.callback( #callback for subject graph
    Output('subject_graph', 'figure'),
    [Input('submit-button-subject', 'n_clicks')],
    [State('my_subject', 'value')])
def update_graph_subject(n_clicks, subject):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    subject_lower = subject.lower()

    # Add traces

    fig.add_trace(
        go.Scatter(x=bt_df.groupby(bt_df.date.dt.to_period('Q'))['compound'].mean().index.to_timestamp(),
                    y=bt_df.groupby(bt_df.date.dt.to_period('Q'))['compound'].mean().values,
                    name="BEATS"),
        secondary_y=False,
    ) #groupby period then take mean of compound score, plot x is time, y is mean compound score



    fig.add_trace(
        go.Scatter(x=bt_df[bt_df['headline_lower'].str.contains(subject_lower, regex=False)].groupby(bt_df.date.dt.to_period('Q'))['compound'].mean().index.to_timestamp(),
                    y=bt_df[bt_df['headline_lower'].str.contains(subject_lower, regex=False)].groupby(bt_df.date.dt.to_period('Q'))['compound'].mean().values,
                    name=subject),
        secondary_y=False,
    ) #add trace of subject


    fig.add_trace( #add article count of subject
        go.Bar(x=bt_df[bt_df['headline_lower'].str.contains(subject_lower, regex=False)].groupby(bt_df.date.dt.to_period('Q'))['compound'].mean().index.to_timestamp(),
                    y=bt_df[bt_df['headline_lower'].str.contains(subject_lower, regex=False)].groupby(bt_df.date.dt.to_period('Q')).size(),
                    name="{} articles".format(subject),
                    opacity=0.5),
        secondary_y=True
    )

    # Add figure title
    fig.layout.update(
        title_text="BEATS index and {}".format(subject)
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="Sentiment", secondary_y=False)
    fig.update_yaxes(title_text="Number of {} articles".format(subject), secondary_y=True)

    return fig

@app.callback( #callback for hover over positive headline
    Output('hover-data-pos', 'children'),
    [Input('subject_graph', 'hoverData'),
    Input('my_subject', 'value')])
def headline_pos_hover(hoverData, subject):
    quarter = hoverData['points'][0]['x'] #get the period (inside 'x'key of a dict within list within dict) u are hovering over, format is "2014-01-01"
    quarter = str(pd.DataFrame({ 'date': pd.to_datetime([quarter])})['date'].dt.to_period('Q')[0]) #convert it into string '2014Q1' through pandas
    subject_lower = subject.lower()

    if bt_df[(bt_df['date'].dt.to_period('Q') == quarter) & bt_df['headline_lower'].str.contains(subject_lower, regex=False)].shape[0] < 6:
        pos_headlines = """
        **Five or fewer articles about {} in {}**
        """.format(subject, quarter)

    else:
        pos_dates = []
        pos_heads = []

        for i in range(3): #cycle through top 3 articles
            pos_dates.append(str(bt_df[(bt_df['date'].dt.to_period('Q') == quarter) & bt_df['headline_lower'].str.contains(subject_lower, regex=False)].nlargest(3, 'compound')['date'].iloc[i]).split()[0]) #convert date to string, split and get date only so time is excluded
            pos_heads.append(bt_df[(bt_df['date'].dt.to_period('Q') == quarter) & bt_df['headline_lower'].str.contains(subject_lower, regex=False)].nlargest(3, 'compound')['headline'].iloc[i])

        neg_dates = []
        neg_heads = []

        for i in range(3): #cycle through top 3 articles
            neg_dates.append(str(bt_df[(bt_df['date'].dt.to_period('Q') == quarter) & bt_df['headline_lower'].str.contains(subject_lower, regex=False)].nsmallest(3, 'compound')['date'].iloc[i]).split()[0]) #convert date to string, split and get date only so time is excluded
            neg_heads.append(bt_df[(bt_df['date'].dt.to_period('Q') == quarter) & bt_df['headline_lower'].str.contains(subject_lower, regex=False)].nsmallest(3, 'compound')['headline'].iloc[i])


        pos_headlines = """**{} Top 3 positive {} articles:**  \n*{}* {}  \n*{}* {}  \n*{}* {}
        """.format(quarter, subject,
                    pos_dates[0], pos_heads[0],
                    pos_dates[1], pos_heads[1],
                    pos_dates[2], pos_heads[2])

    return dedent(pos_headlines)

@app.callback(#callback for hover over negative headline
    Output('hover-data-neg', 'children'),
    [Input('subject_graph', 'hoverData'),
    Input('my_subject', 'value')])
def headline_neg_hover(hoverData, subject):
    quarter = hoverData['points'][0]['x'] #get the period (inside 'x'key of a dict within list within dict) u are hovering over, format is "2014-01-01"
    quarter = str(pd.DataFrame({ 'date': pd.to_datetime([quarter])})['date'].dt.to_period('Q')[0]) #convert it into string '2014Q1' through pandas
    subject_lower = subject.lower()

    if bt_df[(bt_df['date'].dt.to_period('Q') == quarter) & bt_df['headline_lower'].str.contains(subject_lower, regex=False)].shape[0] < 6:
        neg_headlines = """

        """.format(subject, quarter)

    else:
        neg_dates = []
        neg_heads = []

        for i in range(3): #cycle through top 3 articles
            neg_dates.append(str(bt_df[(bt_df['date'].dt.to_period('Q') == quarter) & bt_df['headline_lower'].str.contains(subject_lower, regex=False)].nsmallest(3, 'compound')['date'].iloc[i]).split()[0]) #convert date to string, split and get date only so time is excluded
            neg_heads.append(bt_df[(bt_df['date'].dt.to_period('Q') == quarter) & bt_df['headline_lower'].str.contains(subject_lower, regex=False)].nsmallest(3, 'compound')['headline'].iloc[i])


        neg_headlines = """**{} Top 3 negative {} articles:**  \n*{}* {}  \n*{}* {}  \n*{}* {}
        """.format(quarter, subject,
                    neg_dates[0], neg_heads[0],
                    neg_dates[1], neg_heads[1],
                    neg_dates[2], neg_heads[2])

    return dedent(neg_headlines)

if __name__ == '__main__':
    app.run_server()
