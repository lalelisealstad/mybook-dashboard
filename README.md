# My Books Dashboard

An interactive dashboard app where users can upload their Goodreads library and view statistics about their reading habits and books read. The app is deployed with Cloud Run and is available at: [https://mybook-dashboard-qytxiv2xfq-lz.a.run.app/](https://mybook-dashboard-qytxiv2xfq-lz.a.run.app/)

Screenshots of dashboard: 
![Screenshot 2024-08-06 at 16 03 38](https://github.com/user-attachments/assets/41e2637f-aa4e-4286-940d-02c87eac251a)
![Screenshot 2024-08-06 at 16 06 58](https://github.com/user-attachments/assets/b5e0b32f-f224-4d16-886f-d8d1a880ce93)

I first developed the code in Jupyter notebooks and then export the modules to Python files to be used in the dashboard. The dashboard is written using the Python libraries Dash and Plotly, and it is mobile responsive. I use two public APIs that collects meta data about the books the user uploads. Since the meta data from the APIs did not contain book genre(s) I trained and implemented a multi-label classification machine learning model to automatically predict book genres. I plan on improving the dashboard to show the user a dedicated page for recommendations on what books to read next based on their reading habits. 

# Dashboard components
- Upload component so users can upload their own Goodreads library and see it visualized
- Using a spinner for visual indication that a file is being uploaded
- Created a data pipeline for uploaded data: cleaning data and collecting metadata
- Using asynchronous programming for collecting metadata faster
- Plotly figures to visualize reading habits
- Trained and implemented machine learning model to predit book genres
- Mobile responsive layout

###  Data Extraction and Transformation
Using dash upload component, the user can upload their Goodreads library. The uploaded dataset of the books are cleaned and meta data is collected using APIs. 
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

### Asynchronous API requests
- Using asynchronous code for the Google Books API calls to run batch requests asynchronously, making the dashboard faster and avoiding to exceed the Google Books request quota. 

### Data Visualization

My read books:
- Books read timeline, line chart
- Timeline showing when books were written vs rating
- Distribution of pages, bar chart
- Distribution of languages, pie chart
- Pie chart categories
- Top and bottom books by my rating with other ratings
- Most read authors by count
- Rating of most read authors
- This year in books: total books and total pages
- Tree figures showing category and topics in books
- Visualize genre:
    - Show spider figure for how often genres are read and how well they are rated
    - Bar and bubble combined
    - Show stacked distribution plot, time plot with different lines for genres to see certain times when a genre has been popular


### Machine Learning Model to Predict Genres of Book
The dashboard app automatically preditcs the genres of uploaded books using a machine learning model I trained using sckikit-learn. The ML predits the genres using book descriptions collected from the Google Books API. 

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
```

Docker deployment in gcp: 
```
$ gcloud auth login
$ gcloud auth configure-docker
$ docker build --platform linux/amd64 -t gcr.io/mybookdashboard/mybook-dashboard:1.96 .
$ docker push gcr.io/mybookdashboard/mybook-dashboard:1.96

$ gcloud run deploy mybook-dashboard \
      --image=gcr.io/mybookdashboard/mybook-dashboard:1.96 \
      --platform=managed \
      --region=europe-north1 \
      --timeout=800 \
      --concurrency=800 \
      --cpu=1 \
      --memory=1Gi \
      --max-instances=8 \
      --allow-unauthenticated
```
Latest version: tag 1.96

# Future improvements

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
