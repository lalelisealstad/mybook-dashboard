
Run first time: 
'''
$ python3 -m venv .venv
$ source .venv/bin/activate 
$ pip install pipenv
$ pipenv shell
$ pipenv install ipykernel
$ pipenv install 
'''

run after installation: 
'''
$ source .venv/bin/activate
$ python "app.py"
'''

## Process, see notebooks: 
I first make the code in notebooks and then export the modules in python files to be used in the dahboard. 

#### 1 wpf export
Collect dataframe of Womens prize for fiction winners and finalists with Book Title, Author and year. 
- Use webscraping to collect the table of finalists and winners of the WPF from all years
    - manipulate table to account for merged cells
    - use regex to remove unnecessary signs in the title name

## 2 Data preperation
**Collect metadata from APIs and clean data**

- Collect information about the book using Google Book API
    - API request for book using title and author, if not found then it checks for title with the added strin ': A novel' as I found many books had this title ending in Google Books but not in the WPF wikipedia page, then if book is not found it checks for just title 
    - Normalise string of Title to adjust for Python's case sensitivity before mergning datasett from webscraping wikipeda and google books api

- Collect topics from Open Library API and store as a JSON file
    - To make the topics easy to extract and use I store the information from the OL api as a dictionary with the Title as the Key and the list of topics as the value. 

- Data cleaning / manipulation
    - for the average rating for top authors, NA for My_rating uses mean imputation, so the average rating per author (excluding the 0 or NA values) are imputed as the rating. 
    - na for date_read uses date_added
    - page count category
    - year and quarter read
    - mean impuation for missing rating of top author books

## 3 Asyncronous queries 
- using asyncronous code for the google books api call to run all requests asyncronously 
- making dashboard faster 


## 4 Data Vizualisation
My read books - viz : 
- books read timeline, line chart
- timeline showing when books were written, barchart
- distribution of pages, bar chart
- distribution of languages, pie chart
- pie chart categories, 
- top and botton books my rating with other ratings 
- most read authors by count, and most liked authors 
- this year in books, total books and total pages. 
- tree figures showing category and topics in books 
- scatter pot to visualize if rating and populatity correlate 


## Dashboard components: 
- upload component so user can upload their own Goodreads library and see it visualised
- using a spinner for visual indication that file is being uploaded
- created a datapipeline for uploaded data: cleaning data and collecting metadata
- using asynronous programming for collecting metadata faster 


# Developing: 

## to do:
- genre prediciton using machine learning.
- mobile layout 
- want to read section. 


## Interactivity dashboard:
- date read filter. 
- ratings select filter. 
- poplarity filter. 
- find books based on word or topic: show a list of the books. 

#### Improve performance / layout: 
- set up of topics in json not necessary in case of input
- 0 rating should be changed to "not rated" in the ratings bar. 
- text that explains how to interact with the figures. 
- link to github / explainer of how the dashboard, api call collection works. 
- align first two graphs
- improve speed using client side callbacks 
- improve api call, with await functions - improve the asyncronous, I syspect they are not really asyncronous now 


## What to read next section: 
Want to read: 
- top five rated books 
- top five popular books based on rating count
- books from your top authors
WPF: 
- top five rated books 
- top five popular books based on rating count
- books from your top authors


# Genre categorisation ML 
Multi-label classification to predict multiple genres from book description
- data exploration: most common words 
- data cleaning, make all lower case, remove non alphabeth, non english text, 
- vectorise description and binarize label
- store models 
- reuse model for my books dataet
- create python program file to predict genre using stored models in the app!


Vizualise genre: 
    - show spider figure how often read genre, how well one rate genre
    - show time plot with all different lines for genre to see certains times genre has been popular for one
    - sunburst with other topics around 


## ML Segment analysis for what to read next 
- Ai recommend books want to read based on books read, segment analysis. 
recommendations: 
    - WPF
    - Want-to-read section
    - Best books on good reads https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks

## Other 
- using ai to find male or female author, illustrate distribution 
