
hello

Run: 
$ source venv/bin/activate 
$ pip install pipenv
$ pipenv install -r requirements.txt

alternativ nå: 
pip install -r requirements.txt

## 1_export_data 
Collect dataframe of Womens prize for fiction winners and finalists with Book Title, Author and year. 
- Use webscraping to collect the table of finalists and winners of the WPF from all years
    - manipulate table to account for merged cells
    - use regex to remove unnecessary signs in the title name

## 2_data_cleaning 
Using export of books from Good reads, add additional book information using APIs, do some data cleaning 
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

## Data Vizualisation
My read books - viz : 
- books read timeline, line chart
- timeline showing when books were written, barchart
- distribution of pages, bar chart
- distribution of languages, pie chart
- pie chart categories, 
- top and botton books my rating with other ratings 
- most read authors by count, and most liked authors 
- this year in books, total books and total pages. print


# Developing: 
What to read next section: 
    Want to read: 
    - top five rated books 
    - top five popular books based on rating count
    - books from your top authors

    WPF: 
    - top five rated books 
    - top five popular books based on rating count
    - books from your top authors

Add interactive filter/selection component to dash: 
Book Topics and filter: 
filter on rating, populatiry, 
- Get words from summary. Show most common words, create that into a dictionary like the topics and use word cloud. 
- book topics tree map

Other visualisations: 
- visualise distrobution of ratings, bar chart of count of rated books per rating. 

Other pages:
- Ai recommend books want to read based on books read, segment analysis. 
- using ai to find male or female author, illustrate distribution 


Not doable: 
* similar books using https://www.gutenberg.org/ebooks/20194/also/ - didnt get any books when I did the api call.... 



