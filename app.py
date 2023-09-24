import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd 
import json
import numpy as np
from apps.viz import *
from apps.dataimport import *
from apps.collect_data import *
from datetime import datetime
import pickle 
import base64
import io

#################

mybooks = pd.read_pickle("assets/my_books.pkl")
myreads = mybooks.loc[mybooks['Exclusive_Shelf'] == "read"]
with open('assets/my_topics.json') as file:
    json_data = json.load(file)
my_topics = dict(json_data)
my_read_topics = {k: v for k, v in my_topics.items() if k in myreads.Title.to_list()}  

# Finding todays year and the text for subtitle
today_year = datetime.today().year

#  Create a Dash web application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Define the layout of the app with rows and columns using Bootstrap grid system
app.layout = html.Div([
        html.Div([
            dbc.Container([
                dbc.Row(
                    dbc.Col(
                        [
                            html.H1("Visualising my read books", className="my-4 text-center",style={'color': '#2B2B35', 'text-align': 'center'},),
                            html.H6("Using Goodreads library export with Open Library API and Google Books API", style={'color': '#2B2B35', 'text-align': 'center'},),
                        ],
                    # width={'size': 12, 'offset': 2}
                )
            , style={'background-color': '#FFEFFF'}),
            
            # row to upload books 
            dbc.Row([
                dbc.Col(
                        dcc.Markdown(id='data-info-text', dangerously_allow_html=True, style={'font-size': '16px'}),
                    width=6  # Width for the second column
                ),
                dbc.Col(
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files', style={'color': 'blue', 'font-weight': 'bold'})
                        ]),
                        style={
                            'width': '100%',
                            'height': '80px',
                            'lineHeight': '80px',
                            'borderWidth': '2px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        multiple=False  # Allow only one file upload at a time
                    ),width=6 
                ),
            ], className="mt-4", style={'height': '120px'}), 
            
            # row with text summarising year in books
            # dbc.Row([
            #     dbc.Col(
            #             html.Div(id='data-info-text'),
            #             # (f"This year I have read over {len(myreads.query('Year == @today_year'))} books. Totaling {f'{(myreads.Number_of_Pages.sum().astype(int)):,}'} pages read!", style={'color': '#2B2B35', 'text-align': 'center'}),
            #         width=12 
            #     ),
            # ], className="mt-4", style={'height': '60px'}), 

            # First row with figures
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='fig1',
                        # figure=viz_pub_year(myreads),
                    ),
                    width=6  # Width for the first column
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fig2',
                        figure=viz_year_read(myreads)
                    ),
                    width=6  # Width for the second column
                ),
            ],className="mt-2"),

            # Second row with bar charts
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='fig3',
                        figure=visualize_page_categories(myreads, 'My_Rating', 'How do I rate my books?<br><span style="font-size: 8px;">Number of books per Ratings category</span>', 'Goodreads rating')
                    ),
                    width=6  
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fig4',
                        figure=visualize_page_categories(myreads, 'Page_Cat', 'How long are the books I read?<br><span style="font-size: 8px;">Number of books per Page Count Category</span>', 'Page Count Category')
                    ),
                    width=6 
                ),
            ], className="mt-0"),  # Add margin top

            # Third row - pie charts
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='pie1',
                        figure=viz_top_values(myreads['Language'], top_n=7)
                    ),
                    width=6  
                ),
                dbc.Col(
                    dcc.Graph(
                        id='pie2',
                        figure=viz_top_values(myreads['Categories'], top_n=7)
                    ),
                    width=6  
                ),
            ], className="mt-0"),  

            # Tables
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tbl1',
                        figure=create_rating_table(myreads)
                    ),
                    width=5 
                    ),
                dbc.Col(
                    dcc.Graph(
                        id='tbl2',
                        figure=create_author_table(myreads)
                    ),
                    width=7  
                ),
            ], className="mt-0"),   

            # Rows for bottom and top rated books
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='figr1',
                        figure=book_ratings(myreads, 'Top Rated Books', top_rated=True, show_legend=True)
                    ),
                    width=12 
                    ),
            ], className="mt-0"), 
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='figr2',
                        figure=book_ratings(myreads, 'Bottom Rated Books',top_rated=False, show_legend=False)
                    ),
                    width=12  
                ),
            ], className="mt-0"),  
            
            # Sixth row with desc fig
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tree1',
                        figure=desc_tree(myreads['Description'])
                    ),
                    width=12 
                ),
            ], className="mt-0", style={'height': '420px'}), 

            # Seventh row with topic fig
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tree2',
                        figure=tree_topics(my_read_topics)
                    ),
                    width=12  
                ),
            ], className="mt-0"), 
        ], fluid=True),
    ], style={'margin': '0 40px'}),  
])

 ### CALLBACKS


# Initialize an empty DataFrame to store uploaded data
uploaded_data = pd.DataFrame()
my_read_topics = {}

# Callback to update the line chart with uploaded data
@app.callback(
    [Output('fig1', 'figure'), Output('data-info-text', 'children')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_figure(contents, filename):
    global myreads, my_read_topic
    
    if contents is None:
        # Use the default data if no file is uploaded
        if uploaded_data.empty:
            # Load your default data
            mybooks = pd.read_pickle("assets/my_books.pkl")
            myreads = mybooks.loc[mybooks['Exclusive_Shelf'] == "read"]
            with open('assets/my_topics.json') as file:
                json_data = json.load(file)
            my_topics = dict(json_data)
            my_read_topics = {k: v for k, v in my_topics.items() if k in myreads.Title.to_list()}  
            uploadtxt_sug =  """See your reading stats by uploading your Goodreads library export here:
                            <br><span style="font-size: 12px;">
                            How to find and export Goodreads library:
                            <br>
                            1. Go to [your Goodreads profile](https://www.goodreads.com/)<br>
                            2. Click on "My Books"<br>
                            3. Scroll down and click on "Import/Export" under "Tools" on the left sidebar<br>
                            4. Click "Export Your Books" to download the export file</span>"""
            return viz_pub_year(myreads), uploadtxt_sug

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        new_data = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        new_data = new_data.loc[new_data['Exclusive Shelf'] == "read"]
        nmy_read_topics, nmyreads = dataprep(new_data)
        nmy_read_topics = dict(nmy_read_topics)
        uploadtxt_suc = "Success, your data have been uploaded and the figures updated!"
        return viz_pub_year(nmyreads), uploadtxt_suc
    except Exception as e:
        print(str(e))
        uploadtxt_fail = "Upload failiure...Are you using the csv file from Goodreads export?"
        return viz_pub_year(myreads),  uploadtxt_fail



#desc_tree(mybooks['Description'])
if __name__ == '__main__':
    app.run_server(debug=True)