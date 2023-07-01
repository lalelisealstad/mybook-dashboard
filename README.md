
hello

Run: 
$ source venv/bin/activate 
$ pip install pipenv
$ pipenv install -r requirements.txt

alternativ nå: 
pip install -r requirements.txt



# Pipeline
- Use webscraping to collect the table of finalists and winners of the WPF from all years
    - manipulate table to account for merged cells
    - use regex to remove unnecessary signs in the title name

- Collect information about the book using Google Book API
    - API request for book using title and author, if not found then it checks for title with the added strin ': A novel' as I found many books had this title ending in Google Books but not in the WPF wikipedia page, then if book is not found it checks for just title 
    - Normalise string of Title to adjust for Python's case sensitivity before mergning datasett from webscraping wikipeda and google books api

- Collect topics from Open Library API and store as a JSON file
    - To make the topics easy to extract and use I store the information from the OL api as a dictionary with the Title as the Key and the list of topics as the value. 

Vizualisation:
My read books: 
- book topics tree map
- books read timeline, line chart
- timeline showing when books were written, barchart
- distribution of pages, bar chart
- distribution of languages, pie chart
- pie chart categories, 
- top and botton books use plot with own rating minus goodreads, then center 0 at middle of axis. axis lined along y axis, so opposite way as usual. 

- most read authors by count, and most liked authors 
- this year in books, total books and total pages, cummulative line chart for number of books timeline with number of pages as density chart. Show the number as the indicator plotly, just eh number of pages and books. 

Want to read: 
- top five rated books 
- top five popular books based on rating count

Other pages:
- sentiment analysis of description books. wpf vs own books read vs books want to read
- segment analysis books read
- Ai recommend books want to read based on books read
- using ai to find male or female author

maybe ideas: 
- top five books rates vs other ratings, with rating count

OLD: 
* Store Data in BigQuery 
* Use Open Library API to get the rating, summary and tipcs. 
* Use Google Trends to get the google searches for all the books and WPF in general 
* country auther from wikipedia
* price from Google Book API
* Imput your own books into rhe dashboard - see WPF books matching in seniment, see books that are relevant from WPH using the google books api. 
* similar books using https://www.gutenberg.org/ebooks/20194/also/ 

Key points: 
- pages in book 
- rating 
- country 
- popularity
- sentiment from summaries of books
- ai segmentation av bøker so, jeg ønsker å lese
- 



