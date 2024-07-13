# My Books Dashboard

Create a dashboard app where users can upload their Goodreads library and view statistics about their reading habits and books read. Available at: [https://mybook-dashboard-qytxiv2xfq-lz.a.run.app/](https://mybook-dashboard-qytxiv2xfq-lz.a.run.app/)

I first develop the code in Jupyter notebooks and then export the modules to Python files to be used in the dashboard. See the notebooks described below for the process. The dashboard is written using the Python libraries Dash and Plotly, and it is mobile responsive. I use two public APIs that collects meta data about the books the user uploads. Since the meta data from the APIs did not contain book genre(s) I trained and implemented a multi-label classification machine learning model to automatically predict book genres. 

### 2. Data Extraction and Transformation

**Collect metadata from APIs and clean data**

- **Collect information about the books using the Google Books API**
    - API request for books using title and author

- **Collect topics from the Open Library API and store as a JSON file**
    - To make the topics easy to extract and use, I store the information from the OL API as a dictionary with the title as the key and the list of topics as the value.

- **Data cleaning / manipulation**
    - For the average rating for top authors, NA for My_rating uses mean imputation, so the average rating per author (excluding the 0 or NA values) is imputed as the rating.
    - NA for date_read uses date_added
    - Page count category
    - Year and quarter read
    - Mean imputation for missing ratings of top author books

### 3. Asynchronous Queries

- Using asynchronous code for the Google Books API calls to run all requests asynchronously, making the dashboard faster.

### 4. Data Visualization

My read books - viz:
- Books read timeline, line chart
- Timeline showing when books were written, bar chart
- Distribution of pages, bar chart
- Distribution of languages, pie chart
- Pie chart categories
- Top and bottom books by my rating with other ratings
- Most read authors by count
- Rating of most read authors
- This year in books: total books and total pages
- Tree figures showing category and topics in books
- Scatter plot to visualize if rating and popularity correlate
- Visualize genre:
    - Show spider figure for how often genres are read and how well they are rated
    - Bar and bubble combined
    - Show stacked distribution plot, time plot with different lines for genres to see certain times when a genre has been popular

### Dashboard Components in app.py

- Upload component so users can upload their own Goodreads library and see it visualized
- Using a spinner for visual indication that a file is being uploaded
- Created a data pipeline for uploaded data: cleaning data and collecting metadata
- Using asynchronous programming for collecting metadata faster
- Mobile responsive layout

### 5.2 Machine Learning Model to Predict Genres of Book

Multi-label classification to predict multiple genres from book descriptions
- Data exploration: most common words
- Data cleaning: make all lowercase, remove non-alphabetic characters, non-English text
- Vectorize description and binarize label
- Store models
- Reuse model for my books dataset
- Created Python program file to predict genre using stored model in the app!



## Run the app or the notebooks 
Run first time: 
```
$ python3 -m venv .venv
$ source .venv/bin/activate 
$ pip install -r requirements.txt
$ pip install ipykernel
```

run after installation: 
```
$ source .venv/bin/activate
$ python "app.py"
```

## Deployment notes: 
Docker deploy locally: 
Docker deployment in gcp: 
```
$ docker build -t mybook-dashboard . 
$ docker run -p 8080:8080 mybook-dashboard 

Docker deployment in gcp: 
```
$ gcloud auth login
$ gcloud auth configure-docker
$ docker build --platform linux/amd64 -t gcr.io/mybookdashboard/mybook-dashboard:1.95 .
$ docker push gcr.io/mybookdashboard/mybook-dashboard:1.95

$ gcloud run deploy mybook-dashboard \
      --image=gcr.io/mybookdashboard/mybook-dashboard:1.95 \
      --platform=managed \
      --region=europe-north1 \
      --timeout=1000 \
      --concurrency=100 \
      --cpu=2 \
      --memory=2Gi \
      --max-instances=10 \
      --allow-unauthenticated

Latest version: tag 1.95

### Interactivity dashboard:
- dates to view filter 

## what to read next page: 
- ratings select filter.  
- find books based on word or topic: show a list of the books. 
- genre
- top authors filter, or author select 

### ML Segment analysis for what to read next 
- Ai recommend books want to read based on books read, segment analysis. 
recommendations: 
    - WPF
    - Want-to-read section
    - Best books on good reads https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks

#### WPF: 
- top five rated books 
- top five popular books based on rating count
- books from your top authors


### Use api to give single books insights
 example, this is the longest book you have read and show pic of book