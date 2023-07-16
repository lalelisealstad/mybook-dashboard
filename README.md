
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

- Data cleaning / manipulation
    - 
    - for the average rating for top authors, NA for My_rating uses mean imputation, so the average rating per author (excluding the 0 or NA values) are imputed as the rating. 
    - na for date_read uses date_added
    - page count category
    - year and quarter read
    - mean impuation for missing rating of top author books

Vizualisation:
Done: 
My read books - viz : 
- book topics tree map
- books read timeline, line chart
- timeline showing when books were written, barchart
- distribution of pages, bar chart
- distribution of languages, pie chart
- pie chart categories, 
- top and botton books use plot with own rating minus goodreads, then center 0 at middle of axis. axis lined along y axis, so opposite way as usual. 
- most read authors by count, and most liked authors 
- this year in books, total books and total pages. print

to-do: 
- Get words from summary. Show most common words, create that into a dictionary like the topics and use word cloud. create filter on this: myreads, my want to reads, my rate 5 books, whp books, 

Want to read: 
- top five rated books 
- top five popular books based on rating count

WPF: 
- top five rated books 
- top five popular books based on rating count

Other pages:
- Ai recommend books want to read based on books read
- using ai to find male or female author

OLD: 
* Use Google Trends to get the google searches for all the books and WPF in general 
* country auther from wikipedia
* price from Google Book API
* Imput your own books into rhe dashboard - see WPF books matching in seniment, see books that are relevant from WPH using the google books api. 

Not doable: 
* Store Data in BigQuery  - no point
* Use Open Library API to get the rating, summary and tipcs.  - it is not good 
* similar books using https://www.gutenberg.org/ebooks/20194/also/ - didnt get any books when I did the api call.... 


Key points: 
- pages in book 
- rating 
- country 
- popularity
- sentiment from summaries of books
- ai segmentation av bøker so, jeg ønsker å lese
- 



