from os import link
from re import template
import numpy as np
import dash
import pandas as pd
import plotly.express as px
import geopandas as geo
from dash import Dash, dcc, html, Input, Output  
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv("Data_final.csv")
df['Year-add'] = df['Date_added'].str.split(',').str[1]
df['Year-add'] = df['Year-add'].fillna(0)
df['Year-add'] = df['Year-add'].astype(int, errors = 'raise')
unique_cast = [val.strip() for sublist in df.Cast.dropna().str.split(",").tolist() for val in sublist]

map = pd.read_json('custom.geo.json')

app = dash.Dash(__name__)
server = app.server



# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('netflix_logo.png'),
            id = 'netflix_logo',
            style = {'height' : '60px', 'margin-left' : 'auto', 'margin-right' : 'auto', 'margin-top' : '30px',
            'display':'Block', 'width' : 'auto'},
                 ),
        ],),


        html.H2(children = "Interactive Dashboard", className ='app-header--title',
            style = { 'text-align': 'center',
            'display' : 'block',
            'color': '#F4F4F4',
            'font-size' : '20px',
            },),
        html.Br(),

    html.Div([
        

    ]),
    html.Div([
        dcc.Dropdown(id="slct_year",
                 options=[{'label' : c, 'value' : c}
                    for c in (df["Year-add"].unique())], className ='dcc_compon',
                 multi=False,
                 value=2021,
                 style={'width': "%",
                 'template' : 'plotly_dark'}
                 ),
        dcc.Graph(id='pie_chart', figure={}),
        html.P(children = 'Total Actor and Actress',
            style = {
                'text-align' : 'center',
                'color' : 'white',
                'font-size' : '16px',
                'margin-top' : '5px'
            }),

        html.P(str(len(unique_cast)),
           style = {'color' : 'red',
            'text-align' : 'center',
            'font-size' : '28px',
            'margin-top' : '4px',
            'margin-bottom' : '30px',
            'font-weight' : 'bold'})
    ],className = 'card_container three columns'),

    html.Div([
        dcc.Graph(id='map', figure={}, className = "card_container six columns"),
        dcc.Graph(id='treemap_genre', figure={}, className = "card_container three columns"),
        
    ]),
    
    

    html.Div([
        html.Div([
            html.H2(children = "Opportunity Ahead", className ='app-header--title',
            style = { 'text-align': 'center',
            'display' : 'block',
            'color': 'red',
            'font-size' : '20px',
            'margin-top' : '400px'
            },)
        #    html.P(children = 'Total Actor and Actress',
        #    style = {
        #        'text-align' : 'center',
        #        'color' : 'white',
        #        'font-size' : '16px'
        #    }),

        ##    html.P(str(len(unique_cast)),
        #    style = {'color' : 'red',
        #    'text-align' : 'center',
        #    'font-size' : '32px',
        #    'margin-top' : '4px'

            ])
        ]),
        
        html.Div([
            dcc.Graph(id = 'rating_bar', figure={}, className= "card_container seven columns" ),
            dcc.Graph(id = 'sunburst', figure = {}, className= "card_container five columns")

        ]),
        html.Br(),

        html.Div([
            dcc.Graph(id = 'growth_bar', figure={},className= "card_container five columns" ),
            dcc.Graph(id = 'bingewatch', figure={}, className= "card_container seven columns")

        ]),
        html.Br(),

        html.Div([
            html.Div([
                html.H2(children = "Industry Insight", className ='app-header--title',
            style = { 'text-align': 'center',
            'display' : 'block',
            'color': 'red',
            'font-size' : '20px',
            'margin-top' : '400px'
            },)
            ]),
            
            html.Div([
                dcc.Graph(id = 'heatmap', figure = {}, className= "card_container five columns"),
                dcc.Graph(id = 'top_genres', figure={}, className= "card_container seven columns")   

            ]),
            html.Br(), 

            html.Div([
                dcc.Graph(id = 'length_bar', figure = {}, className= "card_container one-half column"),
                dcc.Graph(id = 'language', figure={}, className= "card_container one-half column")
            ]),
            html.Br()
 
            ])
        ]),

    ])


    #html.Div([
    #    html.Div([
    #        html.P('Available Titles: ',
    #        style = 
    #        {'color' : 'white',
    #        'text-align' : 'center',
    #        'font-size' : '16px'
    #        },),
    #        html.H6(str(len(df["Title"])),
    #        style = 
    #        {'color' : 'red',
    #        'text-align' : 'center',
    #        'font-size' : '24px',
    #        'margin-top' : '8px'
    #        })

    #    ], className='card_container three columns'),




#------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (Pie Chart)
@app.callback(
    Output(component_id='pie_chart', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
    )

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    df2 = df.copy()
    df2 = df2[df2['Year-add'] == option_slctd]


    fig = px.pie(df2, values=[(df2["Type"]=='Movie').sum(), (df2["Type"]=='TV Show').sum()],
            names= ["Movies", "TV Show"],
            color_discrete_sequence= px.colors.sequential.Reds_r,
            width = 300, 
            height=300,
            template='plotly_dark')
    fig.update_traces(textposition='inside', textinfo='percent+label', )
    fig.update_layout(
    title={ 'text' : 'Available Titles in ' + str(option_slctd) + ':' + '<br>'  + str(len(df2[df2['Year-add'] == option_slctd])),
        'x' : 0.5,
        'y' : 0.90,
        'xanchor' : 'center',
        'yanchor' : 'top'},
        font={'family' : "Helvetica",
            'size' : 12,
            'color' : 'white',},
            showlegend = False
            )

    return fig

#------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (Maps)
unique_countries = [val.strip() for sublist in df.Country.dropna().str.split(",").tolist() for val in sublist]
country_summary = pd.DataFrame(unique_countries,columns=['Country']).value_counts().reset_index().rename(columns={0:'Count'})
found = []
missing = []
countries_geo = []

# For simpler acces, setting "zone" as index in a temporary dataFrame
tmp = country_summary.set_index('Country')

# Looping over the custom GeoJSON file
for country in map['features']:
    
    # Country name detection
    country_name = country['properties']['name'] 
    
    # Checking if that country is in the dataset
    if country_name in tmp.index:
        
        # Adding country to our "Matched/found" countries
        found.append(country_name)
        
        # Getting information from both GeoJSON file and dataFrame
        geometry = country['geometry']
        
        # Adding 'id' information for further match between map and data 
        countries_geo.append({
            'type': 'Feature',
            'geometry': geometry,
            'id':country_name
        })
        
    # Else, adding the country to the missing countries
    else:
        missing.append(country_name)

# Displaying metrics
geo_world_ok = {'type': 'FeatureCollection', 'features': countries_geo}

country_summary['count_color'] = country_summary['Count'].apply(np.log10)


# Get the maximum value to cap displayed values
max_log = country_summary['count_color'].max()
max_val = int(max_log) + 1

# Prepare the range of the colorbar
values = [i for i in range(max_val)]
ticks = [10**i for i in values]

@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
    )


def update_maps(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    df2 = df.copy()
    df2 = df2[df2['Year-add'] == option_slctd]

    fig = px.choropleth(
        country_summary,
        geojson=geo_world_ok,
        locations='Country',
        color=country_summary['count_color'],
        range_color=(0, country_summary['count_color'].max()),
        hover_data = {'Count':True, 'count_color': False},
        color_continuous_scale='Reds', template = 'plotly_dark',   
    )


# Define layout specificities
    fig.update_layout(
      margin={'r':0,'t':0,'l':0,'b':0}, 
            coloraxis_showscale=False,
            title={ 'text' : 'Netflix is available in' + '<br>' + '123 countries',
        'x' : 0.5,
        'y' : 0.95,
        'xanchor' : 'center',
        'yanchor' : 'top'},
        font={'family' : "Helvetica",
            'size' : 12,
            'color' : 'white'})


    return fig

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (Treemap Genre)
# Memisahkan Genre yang Lebih dari Satu
unique_genres = [val.strip() for sublist in df.Listed_in.dropna().str.split(",").tolist() for val in sublist]
genre_summary = pd.DataFrame(unique_genres,columns=['Listed_in']).value_counts().reset_index().rename(columns={0:'count'})
genre_summary = genre_summary.drop([0,3], axis=0)

@app.callback(
    Output(component_id='treemap_genre', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
    )

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    df2 = df.copy()
    df2 = df2[df2['Year-add'] == option_slctd]

    fig = px.treemap(genre_summary, path=['Listed_in'], values='count', color='count',
                  height=450,
                  color_continuous_scale='Reds',
                  title="Genre Distribution on Netflix",
                  template = 'plotly_dark'
                  )
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25), 
        coloraxis_showscale = False,
         title={ 'text' : 'Genre Distribution',
        'x' : 0.5,
        'y' : 0.95,
        'xanchor' : 'center',
        'yanchor' : 'top'},
        font={'family' : "Helvetica",
            'size' : 12,
            'color' : 'white'})
    fig.update_traces(hovertemplate=None)

    return fig

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (Bar Chart)
title_count = df.groupby('Year-add').count().reset_index()
sorted_year = title_count.sort_values(by='Year-add', ascending=True)
sorted_year_sum = sorted_year.cumsum(axis = 0)

@app.callback(
    Output(component_id='growth_bar', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
    )

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    df2 = df.copy()
    df2 = df2[df2['Year-add'] == option_slctd]

    fig = px.bar(sorted_year, x="Year-add", 
        y=sorted_year_sum['Type'], 
        labels={"y":"Total ", "Year-add":"Year "}, 
        color_discrete_sequence= px.colors.sequential.Reds_r,
        height=400,
        template = 'plotly_dark')
    fig.update_layout(bargap=0,
        title={ 'text' : 'The amount of titles has grown exponentially',
        'x' : 0.5,
        'y' : 0.90,
        'xanchor' : 'center',
        'yanchor' : 'top'},
        font={'family' : "Helvetica",
            'size' : 12,
            'color' : 'white',},
            showlegend = False,
            yaxis_range = [0,9000],
            xaxis_range = [2008,2021])

    return fig

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (Sunburst)
sorted_data = df.sort_values(by='IMDB', ascending=False)
sorted_data = sorted_data[0:10]

@app.callback(
    Output(component_id='sunburst', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
    )

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    df2 = df.copy()
    df2 = df2[df2['Year-add'] == option_slctd]

    fig =px.sunburst(sorted_data, path=['IMDB','Title'], 
                 values='IMDB', 
                 color='IMDB',  
                 color_continuous_scale='Reds',
                 height=400,
                 template = 'plotly_dark')
    fig.update_layout(bargap=0,
        title={ 'text' : 'Bunch of IMDB high-rated movies are featured',
        'x' : 0.5,
        'y' : 0.95,
        'xanchor' : 'center',
        'yanchor' : 'top'},
        font={'family' : "Helvetica",
            'size' : 12,
            'color' : 'white',},
            showlegend = False,
            yaxis_range = [0,9000],
            xaxis_range = [2008,2021],
            coloraxis_showscale=False,)
    fig.update_traces(hovertemplate=None)

    return fig

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (Audience Analysis)
Rating_counts = df.groupby('Rating').count().reset_index()
sorted_rating = Rating_counts.sort_values(by='Type', ascending=True)

@app.callback(
    Output(component_id='rating_bar', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
    )

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    df2 = df.copy()
    df2 = df2[df2['Year-add'] == option_slctd]

    fig = px.bar(sorted_rating , 
                x="Rating", y="Type", 
                color="Type", text="Type",
                labels={"Type":"Count"},
                color_continuous_scale='Reds',
                height=400,
                template = 'plotly_dark')

    fig.update_layout(bargap=0.2,
        title={ 'text' : 'The audience is growing and dominated by mature audiences',
        'x' : 0.5,
        'y' : 0.95,
        'xanchor' : 'center',
        'yanchor' : 'top'},
        font={'family' : "Helvetica",
            'size' : 12,
            'color' : 'white',},
            coloraxis_showscale = False,
            yaxis_range = [0,3500])

    return fig

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (Bingewatch)
netflix_shows = df[df['Type']=='TV Show']
netflix_shows["Season"] = netflix_shows['Duration'].astype(str).apply(lambda x : x.lstrip().split(' ')[0])
netflix_shows['Season'] = netflix_shows['Season'].astype(int, errors = 'raise')
filtered_binge = netflix_shows[netflix_shows['Season'] > 7]

@app.callback(
    Output(component_id='bingewatch', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
    )

def update_graph(option_slctd):
    print(option_slctd)
    df2 = df.copy()
    df2 = df2[df2['Year-add'] == option_slctd]

    fig = px.treemap(filtered_binge, 
                    path=['Duration', 'Title'], 
                    values='Release_year', 
                    color_discrete_sequence= px.colors.sequential.Reds_r,
                    height=400,
                    template = 'plotly_dark')

    fig.update_layout(bargap=0.2, margin = dict(t=50, l=25, r=25, b=25),
        title={ 'text' : 'Bingewatch : ' + '<br>' + str(len(filtered_binge)) + ' shows have more than 8 seasons',
        'x' : 0.5,
        'y' : 0.90,
        'xanchor' : 'center',
        'yanchor' : 'top'},
        font={'family' : "Helvetica",
            'size' : 12,
            'color' : 'white',},
            )
    fig.update_traces(hovertemplate=None)

    return fig
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (Heatmap)
netflix_date = df
netflix_date['Year'] = netflix_date['Year-add']
netflix_date['Month'] = netflix_date['Date_added'].astype(str).apply(lambda x : x.lstrip().split(' ')[0])
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][::-1]
df1 = netflix_date.groupby('Year')['Month'].value_counts().unstack().fillna(0)[month_order].T


@app.callback(
    Output(component_id='heatmap', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
    )

def update_graph(option_slctd):
    print(option_slctd)
    df2 = df.copy()
    df2 = df2[df2['Year-add'] == option_slctd]

    fig = px.imshow(df1, 
        color_continuous_scale= px.colors.sequential.Reds,
        template = 'plotly_dark',
        height=400)
    fig.update_layout(bargap=0.2,
        title={ 'text' : 'February is the least crowded month to add new titles',
        'x' : 0.5,
        'y' : 0.95,
        'xanchor' : 'center',
        'yanchor' : 'top'},
        font={'family' : "Helvetica",
            'size' : 12,
            'color' : 'white',},
            coloraxis_showscale = False,
            xaxis_range = [2008,2021])
    fig.update_traces(hovertemplate=None)
    fig.update_traces(hovertemplate='Year: %{x}<br>Month: %{y}<br>Count: %{z}<extra></extra>')
    

    return fig
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (Top Genres)
netflix_movies = df[df['Type']=='Movie']
netflix_shows = df[df['Type']=='TV Show']
#Pengolahan Movies
genre_movies = [val.strip() for sublist in netflix_movies.Listed_in.dropna().str.split(",").tolist() for val in sublist]
summary_movies = pd.DataFrame(genre_movies,columns=['Listed_in']).value_counts().reset_index().rename(columns={0:'count'})
summary_movies = summary_movies.sort_values("count", ascending=True)
#Pengolahan TV Show
genre_shows = [val.strip() for sublist in netflix_shows.Listed_in.dropna().str.split(",").tolist() for val in sublist]
summary_shows = pd.DataFrame(genre_shows,columns=['Listed_in']).value_counts().reset_index().rename(columns={0:'count'})
summary_shows  = summary_shows .sort_values("count", ascending=True)


@app.callback(
    Output(component_id='top_genres', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
    )

def update_graph(option_slctd):
    print(option_slctd)
    df2 = df.copy()
    df2 = df2[df2['Year-add'] == option_slctd]

    subplot = make_subplots(rows=1, cols=2)

    # add the 1st graph by specifying which row and column it will come to
    subplot.add_trace(go.Bar(y=summary_movies["Listed_in"], 
                    x=summary_movies["count"],
                    name='Movies',
                    orientation='h',
                    marker=dict(color='rgb(229,9,20)')),
                    row=1, col=1,
                    )
    # add the 2nd graph
    subplot.add_trace(go.Bar(y=summary_shows["Listed_in"], 
                    x=summary_shows["count"],
                    name='TV Shows',
                    orientation='h', 
                    marker=dict(color='rgb(255,244,240)')), 
                    row=1, col=2,
                    )

    subplot.update_layout(showlegend=True, template = 'plotly_dark', height = 400)
    subplot.update_layout(title={ 'text' : 'Top Genres Comparison between TV Shows and Movies',
        'x' : 0.5,
        'y' : 0.95,
        'xanchor' : 'center',
        'yanchor' : 'top'},
        font={'family' : "Helvetica",
            'size' : 12,
            'color' : 'white',},
            coloraxis_showscale = False,
            )

    return subplot

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (Length Bar)
netflix_movies = df[df['Type']=='Movie']
netflix_movies['Duration'] = netflix_movies['Duration'].astype(float, errors = 'raise')
sorted_duration = netflix_movies.sort_values(by='Duration', ascending=True)

@app.callback(
    Output(component_id='length_bar', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
    )

def update_graph(option_slctd):
    print(option_slctd)
    df2 = df.copy()
    df2 = df2[df2['Year-add'] == option_slctd]

    fig = px.bar(sorted_duration[6118:6128] , y="Title", x="Duration", 
        orientation='h', 
        color_discrete_sequence=px.colors.sequential.Reds_r,
        title = 'Some Movies are Lengthy Movie',
        height = 400,
        template = 'plotly_dark')
    fig.update_layout(title={ 'text' : 'Some movies are lengthy movie',
        'x' : 0.5,
        'y' : 0.95,
        'xanchor' : 'center',
        'yanchor' : 'top'},
        font={'family' : "Helvetica",
            'size' : 12,
            'color' : 'white',},
            coloraxis_showscale = False,
            )

    
    return fig
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components (Language)
unique_Language = [val.strip() for sublist in df.Language.dropna().str.split(",").tolist() for val in sublist]
language_summary = pd.DataFrame(unique_Language,columns=['Language']).value_counts().reset_index().rename(columns={0:'Count'})

@app.callback(
    Output(component_id='language', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
    )

def update_graph(option_slctd):
    print(option_slctd)
    df2 = df.copy()
    df2 = df2[df2['Year-add'] == option_slctd]

    fig = px.treemap(language_summary, path=['Language'], values='Count', color='Count',
                  color_continuous_scale='Reds',
                  height=400,
                  template = 'plotly_dark'
                  )
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25),
        coloraxis_showscale = False,
        title={ 'text' : "Almost half of the titles use English",
        'x' : 0.5,
        'y' : 0.95,
        'xanchor' : 'center',
        'yanchor' : 'top'},
        font={'family' : "Helvetica",
            'size' : 12,
            'color' : 'white'}
    )
    fig.update_traces(hovertemplate=None)

    return fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
