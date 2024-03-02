
#### Run the app or the notebooks 
Run first time: 
```
$ python3 -m venv .venv
$ source .venv/bin/activate 
$ pip install pipenv
$ pipenv install ipykernel
$ pipenv install 
```

run after installation: 
```
$ source .venv/bin/activate
$ python "app.py"
```

Docker deploy locally: 
$ docker build -t mybook-dashboard . 
$ docker run -p 8080:8080 mybook-dashboard 

Docker deployment in gcp: 
```
$ gcloud auth login
$ gcloud auth configure-docker
$ docker build --platform linux/amd64 -t gcr.io/mybookdashboard/mybook-dashboard .
$ docker tag mybook-dashboard gcr.io/mybookdashboard/mybook-dashboard:1.0
$ docker push gcr.io/mybookdashboard/mybook-dashboard:1.0

$ gcloud run deploy mybook-dashboard \
      --image=gcr.io/mybookdashboard/mybook-dashboard:1.0 \
      --platform=managed \
      --region=europe-north1 \
      --timeout=60 \
      --concurrency=80 \
      --cpu=1 \
      --memory=256Mi \
      --max-instances=10 \
      --allow-unauthenticated

increased memory - now it is working! 

# Documentation of process: 
I first make the code in notebooks and then export the modules in python files to be used in the dahboard. 
See the notebooks as described below for the process. The notebooks can be run seperately from the app. 

## 1 wpf export
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
- Vizualise genre: 
    - show spider figure how often read genre, how well one rate genre
    - bar and bubble combined
    - show stacked distribution plot, time plot with all different lines for genre to see certains times genre has been popular for one


## Dashboard components in app.py: 
- upload component so user can upload their own Goodreads library and see it visualised
- using a spinner for visual indication that file is being uploaded
- created a datapipeline for uploaded data: cleaning data and collecting metadata
- using asynronous programming for collecting metadata faster 
- mobile responsive layout. 


## 5.2 Machine Learning model to predict genres of book
Multi-label classification to predict multiple genres from book description
- data exploration: most common words 
- data cleaning, make all lower case, remove non alphabeth, non english text, 
- vectorise description and binarize label
- store models 
- reuse model for my books dataet
- create python program file to predict genre using stored models in the app!


# Developing: 
- make px padding smaller 
- adjust legends on the top and bottom rated authors, not nice on mobile 
- bok description three fig title should be shorter 
- adjust legends for popularity fig too, title not showing
- adjust text size for lgends and maybe even ledengs to be below for time genre fig, and title and subtitle too long 
- try and remove whitespace on figures mobile: fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
)


- add row w a panel with incons showing some quick stats over books read the last year or month.
- change tables to, horisontal figure, one with mean rating top and count of read books by authors. 
- check all text, make similar to story graph
- 0 rating should be changed to "not rated" in the ratings bar. 
- text that explains how to interact with the figures. 
- number of books read in year querter have subtext going into the graph


## Interactivity dashboard:
- dates to view 
what to read next: 
- ratings select filter.  
- find books based on word or topic: show a list of the books. 
- genre
- top authors filter, or author select 

#### Improve performance / layout:
- remove prints and use logging instead. 
- set up of topics in json not necessary in case of input
- link to github / explainer of how the dashboard, api call collection works. 
- improve speed using client side callbacks 
- store data in google cloud
- store inputted data in google cloud. 
- warning for user when max capasity in Google books api quota is reached 
- loading bar with percentage when uploading books with estimate of time left. 


## What to read next section: 
Want to read: 
- top five rated books 
- top five popular books based on rating count
- books from your top authors
- top books in most liked genres. 

WPF: 
- top five rated books 
- top five popular books based on rating count
- books from your top authors


## ML Segment analysis for what to read next 
- Ai recommend books want to read based on books read, segment analysis. 
recommendations: 
    - WPF
    - Want-to-read section
    - Best books on good reads https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks

## Other 
- using ai to find male or female author, illustrate distribution 
