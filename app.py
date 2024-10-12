import dash
from dash import html, dcc, page_registry
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import logging

# Configure logging to see errors in GCP
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a Dash web application
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LUX],
                use_pages=True,  # Ensure this flag is true to enable the pages feature
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=0.9, maximum-scale=1.2, minimum-scale=0.5,'}]
                )

app.title = 'Book Dashboard'

# Define the layout of the app
app.layout = html.Div([
    html.Div([
        dbc.Container([
            dbc.Row(
                dbc.Col(
                    [
                        html.H1("Book Dashboard", className="my-4 text-center heading"),
                        html.P("Welcome to the Book Reading Statistics Dashboard. Explore insightful data about your reading habits and uncover new insights into your literary adventures!",
                               className="subheading"),
                    ],
                    className='five columns box-background')
            , justify="center"),

            # Row to upload books
            dbc.Row([
                dbc.Col(
                    [
                        dcc.Markdown(id='data-info-text1', dangerously_allow_html=True, className="markdown-large"),
                        dcc.Markdown(id='data-info-text2', dangerously_allow_html=True, className="markdown-small"),
                    ], xs=10, sm=10, md=10, lg=5, xl=5
                ),
                dbc.Col([
                    dbc.Spinner(children=[
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files', className='upload-link'),
                            ]),
                            className="upload-area",
                            multiple=False),  # Allow only one file upload at a time
                        dcc.Markdown(id='upload-text', dangerously_allow_html=True, className="upload-text"),
                    ])
                ], xs=10, sm=10, md=10, lg=5, xl=5)
            ], className="upload-section", justify="center"),

            # Tabs and page navigation
            html.Div(
                [
                    dcc.Location(id="url", refresh="callback-nav"),
                    dcc.Tabs(
                        id='tabs', 
                        value='tab-1', 
                        children=[
                            dcc.Tab(label='Read', value='tab-1', className="tab", selected_className="tab--selected"),
                            dcc.Tab(label='Want to read', value='tab-2', className="tab", selected_className="tab--selected"),
                        ]
                    ),
                    dash.page_container
                ]
            ),

            # dcc.Store inside the user's current browser session
            html.Div([
                dcc.Store(id='store-data', data=[], storage_type='session'),  # store of the list of read books
                dcc.Store(id='is-uploaded-data', data=[], storage_type='session')  # store binary showing if data is uploaded
            ])
        ], fluid=True),
    ], className="main-container"),
])



@app.callback(
    Output("url", "href"),
    Input("tabs", "value")
)
def update_tab_content(value):  
    if value == "tab-2":
        return "/wanttoread"
    return "/read"


server = app.server  # Get the underlying Flask server instance

# Callbacks should be defined below

if __name__ == '__main__':
    # app.run_server(debug=False, host="0.0.0.0", port=8080, use_reloader=False)  # debug=False in deployment
    app.run_server(debug=True, host="0.0.0.0", port=8080)