
# topics viz tree map

import pandas as pd
import plotly.express as px

def tree_topics(topics_dict): 
    """
    Creates a tree map visualisation of book topics by count
    param: dictionary contaning title of book as key and the value is one list contaning the book's topics
    
    """

    # Prepare the data for the treemap
    data = []
    for title, topics in topics_dict.items():
        for topic in topics:
            data.append({'Title': title, 'Topic': topic})

    df = pd.DataFrame(data)

    # Group by 'Title' and 'Topic' columns and count the occurrences
    grouped_df = df.groupby(['Topic']).size().reset_index(name='Count')

    # Create the treemap figure
    # fig = px.treemap(grouped_df.query('Count > 1'), path=['Topic'], values='Count')
    grouped_df = grouped_df[~grouped_df["Topic"].str.contains('fiction', case=False)]
    # Create the treemap figure
    fig = px.treemap(
        grouped_df.query('Count > 2'),
        path=['Topic'],
        values='Count',
        color='Count',
        color_continuous_scale='Purp',
        hover_name='Topic'
    )

    # Customize the appearance of the treemap
    fig.update_layout(
        title='Book Topics Treemap',
        treemapcolorway=px.colors.sequential.Purp  # Use pretty pastel color palette
    )

    # Set text properties for wrapping
    fig.update_traces(
        textfont=dict(size=14),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'  # Display count on hover
    )

    # Set layout properties for wrapping
    fig.update_layout(
        autosize=True,
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(size=14),
        hoverlabel=dict(font=dict(size=12))
    )

    # Add custom data (Title) to each treemap trace
    fig.data[0].update(customdata=grouped_df['Topic'])
    return fig 


import pandas as pd
import plotly.graph_objects as go
import numpy as np

def viz_pub_year(df):
    # filter na in publication year and make column publication year integer 
    df = df.dropna(subset=['Original_Publication_Year'])
    df['Original_Publication_Year'] = df['Original_Publication_Year'].astype(int)
    # Group the DataFrame by year and calculate the average rating and count of books
    year_data = df.groupby('Original_Publication_Year').agg({'My_Rating': 'mean', 'Title': 'count'}).reset_index()
    
    # Extract the year labels, average ratings, and book counts
    labels = year_data['Original_Publication_Year']
    ratings = year_data['My_Rating']
    book_counts = year_data['Title']
    
    # # Create the hover text with book title, My_Rating, and Original_Publication_Year
    # hover_text = []
    # for year in labels:
    #     books = df[df['Original_Publication_Year'] == year]
    #     hover_text.append(f"<span style='font-size: 16px;'>{year}</span><br>" + '<br>'.join(f"{book['Title']} - Rating: {book['My_Rating']}" for _, book in books.iterrows()))

    hover_text = []
    for year in labels:
        books = df[df['Original_Publication_Year'] == year]
        book_text = ""
        for i, (_, book) in enumerate(books.iterrows()):
            if i >= 19:
                book_text += "..."
                break
            book_text += f"{book['Title']} - Rating: {book['My_Rating']}<br>"
        hover_text.append(f"<span style='font-size: 16px;'>{year}</span><br>" + book_text)

    
    # Scale the bubble sizes based on the logarithm of the count of books
    sizes = np.log(book_counts)  # Logarithmic scaling
    
    # Adjust the scaling factor to increase the size difference
    scaling_factor = 1.5  # Adjust the scaling factor as needed
    sizes = sizes * scaling_factor
    
    # Set a minimum size for bubbles with a count of 1
    min_size = 1  # Adjust the minimum size as needed
    sizes = np.where(book_counts < 2, min_size, sizes)
    
    # Create the scatter plot
    fig = go.Figure(data=go.Scatter(
        x=labels,
        y=ratings,
        mode='markers',
        text=hover_text,
        hoverinfo='text',
        marker=dict(
            size=sizes,
            sizemode='diameter',
            sizeref=sizes.max() / 50,  # Adjust the size scaling factor as needed
            color=ratings,
            colorscale='Sunset',  # Choose a desired color scale
            showscale=True
        )
    ))
    
    # Customize the plot layout
    fig.update_layout(
        title='My Ratings and Publication Year',
        xaxis=dict(title='Publication Years'),
        yaxis=dict(title='My Rating'),
        showlegend=False,
        template = "plotly_white"
    )
    
    return fig

import pandas as pd
import plotly.express as px

def viz_year_read(df):
    # Convert 'Date_Read' column to datetime type
    df['Date_Read'] = pd.to_datetime(df['Date_Read'])
    
    # Extract year and quarter from 'Date_Read' column
    df['Year'] = df['Date_Read'].dt.year
    df['Quarter'] = df['Date_Read'].dt.quarter
    
    # Create a new column combining year and quarter
    df['Year_Quarter'] = df['Year'].astype(str) + '-Q' + df['Quarter'].astype(str)
    
    # Convert Year_Quarter to categorical variable
    df['Year_Quarter'] = pd.Categorical(df['Year_Quarter'], ordered=True)
    
    # Count the number of books read in each year and quarter
    year_quarter_counts = df.groupby('Year_Quarter').size().reset_index(name='Books Read')
    
    # Create the line chart
    fig = px.line(year_quarter_counts, x='Year_Quarter', y='Books Read', markers=True, template = "plotly_white")
    
    # Customize the plot layout
    fig.update_layout(
        title='Number of Books Read per Year and Quarter<span style="font-size: 10px;"><br>Year read is based on when you set the dates read manually, and if no dates where set then the date the book was added is used</span>',
        xaxis=dict(title='Year and Quarter'),
        yaxis=dict(title='Number of Books Read'),
        showlegend=False
    )
    
    # Return the figure
    return fig

### Page count 

import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

def visualize_page_categories(myreads, column):
    # Group the DataFrame by page category and count the number of books in each category
    category_counts = myreads[column].value_counts().sort_index()

    # Assign a unique color to each category
    colors = ['rgb(251,180,174)', 'rgb(179,205,227)', 'rgb(204,235,197)', 'rgb(222,203,228)', 'rgb(254,217,166)', 'rgb(255,255,204)']

    # Create the bar chart
    fig = go.Figure(data=go.Bar(
        x=category_counts.index,
        y=category_counts.values,
        marker=dict(color=colors),
    ))

    # Set the chart title and axis labels
    fig.update_layout(
        title='Number of books per Page Count Category',
        xaxis=dict(title='Page Count Category'),
        yaxis=dict(title='Number of Books'),
        template = "plotly_white"
    )

    # Display the chart
    fig.show()


# pie chart, top 5 categories and languages
import plotly.graph_objects as go

def viz_top_values(column, top_n=10):
    # Drop NaN values from the column
    column = column.dropna()
    # Calculate the value counts of the column
    column_counts = column.value_counts()

    # Select the top values and their counts
    top_values = column_counts.head(top_n)
    labels = top_values.index
    values = top_values.values

    # Define the color theme
    colors = ['rgb(244, 202, 228)','rgb(179, 226, 205)', 'rgb(253, 205, 172)', 'rgb(203, 213, 232)',
               'rgb(230, 245, 201)', 'rgb(255, 242, 174)',
              'rgb(241, 226, 204)', 'rgb(204, 204, 204)', 'rgb(255, 255, 204)',
              'rgb(197, 226, 255)']

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # Set the colors using the color theme
    fig.update_traces(marker=dict(colors=colors))

    # Set the chart title
    fig.update_layout(title=f'Top {top_n} Values of {column.name}')

    # Display the chart
    fig.show()



#### highest and lowest rated books

import plotly.graph_objects as go
import plotly.colors
from plotly.subplots import make_subplots

def plot_book_ratings(data):
    # Filter the data where My_Rating > 0
    filtered_data = data[data['My_Rating'] > 0]

    # Sort the filtered data by your own rating in descending order
    sorted_data = filtered_data.sort_values('My_Rating', ascending=False)

    # Select the top 5 and bottom 5 books based on your own rating
    top_books = sorted_data.head(15)
    bottom_books = sorted_data.tail(10)

    # Create the figure object with subplots
    fig = make_subplots(rows=2, cols=1, subplot_titles=("My highest Rated Books", "My lowest Rated Books"))

    # Define the Pastel1 color scheme
    pastel_colors = plotly.colors.qualitative.Pastel1

    # Add traces for top rated books
    fig.add_trace(go.Bar(
        y=top_books['Title'],
        x=top_books['My_Rating'],
        name='My Rating',
        orientation='h',
        marker=dict(color=pastel_colors[0])
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        y=top_books['Title'],
        x=top_books['Average_Rating_GoogleBooks'],
        name='Average Rating (Google Books)',
        orientation='h',
        marker=dict(color=pastel_colors[1])
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        y=top_books['Title'],
        x=top_books['Average_Rating_Goodreads'],
        name='Average Rating (Goodreads)',
        orientation='h',
        marker=dict(color=pastel_colors[2])
    ), row=1, col=1)

    # Add traces for bottom rated books
    fig.add_trace(go.Bar(
        y=bottom_books['Title'],
        x=bottom_books['My_Rating'],
        name='My Rating',
        orientation='h',
        marker=dict(color=pastel_colors[3])
    ), row=2, col=1)

    fig.add_trace(go.Bar(
        y=bottom_books['Title'],
        x=bottom_books['Average_Rating_GoogleBooks'],
        name='Average Rating (Google Books)',
        orientation='h',
        marker=dict(color=pastel_colors[4])
    ), row=2, col=1)

    fig.add_trace(go.Bar(
        y=bottom_books['Title'],
        x=bottom_books['Average_Rating_Goodreads'],
        name='Average Rating (Goodreads)',
        orientation='h',
        marker=dict(color=pastel_colors[5])
    ), row=2, col=1)

    # Update the layout
    fig.update_layout(
        title='Book Ratings',
        showlegend=False,
        height=900,
        width=800,
        plot_bgcolor='rgba(255, 255, 255, 1)',
        paper_bgcolor='rgba(255, 255, 255, 1)',
        yaxis=dict(title='Title'),
        xaxis=dict(title='Rating'),
        barmode='group'
    )

    # Show the plot
    fig.show()




# Rating compare
import plotly.graph_objects as go

def create_rating_table(data):
    # Filter the data where My_Rating > 0
    filtered_data = data[data['My_Rating'] > 0]

    # Calculate the mean ratings
    mean_ratings = filtered_data[['Average_Rating_GoogleBooks', 'Average_Rating_Goodreads', 'My_Rating']].mean()

    # Create a list of rating names
    ratings = ['My Rating', 'Average Rating (Google Books)', 'Average Rating (Goodreads)']

    # Create a list of mean rating values
    mean_values = np.round(mean_ratings.values.tolist(),3)

    # Create a Plotly table
    table = go.Figure(data=[go.Table(
        header=dict(values=['Rating', 'Mean Rating'],
                    fill_color='rgba(200, 220, 240, 0.5)',
                    align=['left', 'center']),
        cells=dict(values=[ratings, mean_values],
                   fill_color='rgba(220, 235, 245, 0.5)',
                   align=['left', 'center'])
    )])

    # Set the table colors
    table.update_layout(
        template='plotly_white',
        plot_bgcolor='white', 
        width=600
    )


    return table



# My top authors 
import plotly.graph_objects as go
import numpy as np

def create_author_table(data):
    # Filter the data to include only the books you've read
    data = data[data['Author'].isin(data['Author'].value_counts().nlargest(5).index)].copy()

    # Replace 0 by np.nan so its not included in the mean (Usally 0 rating means it is not rated) 
    data['My_Rating'] = data['My_Rating'].replace(0, np.nan)

    # Calculate the mean 'My_Rating' grouped by 'Author'
    data['mean_rating_by_author'] = data.groupby('Author')['My_Rating'].transform('mean').copy()

    data['My_Rating'] = np.where((data['My_Rating'] == np.nan) | data['My_Rating'].isnull(), data['mean_rating_by_author'], data['My_Rating'])

    # Group the data by author and calculate the required statistics
    author_stats = np.round(data.groupby('Author').agg({
        'Read_Count' :'count', 
        'My_Rating': 'mean',
        'Average_Rating_Goodreads': 'mean',
        'Rating_Count': 'sum',
    }).reset_index(),2)

    # Sort the authors based on the mean rating in descending order
    sorted_authors = author_stats.sort_values('Read_Count', ascending=False)

    # Select the top five authors
    top_authors = sorted_authors.head(5)

    # Create a Plotly table
    table = go.Figure(data=[go.Table(
        header=dict(values=['Author', 'Number of books read by author', 'Average Rating', 'Number of times rated on Goodreads', 'Average Goodreads Rating'],
                    fill_color='rgba(200, 220, 240, 1)',
                    align='center', 
                    height=30,),
        cells=dict(values=[top_authors['Author'],
                           top_authors['Read_Count'],
                           top_authors['My_Rating'],
                           top_authors['Rating_Count'],
                           top_authors['Average_Rating_Goodreads']], 
                           fill=dict(color=['rgba(200, 220, 240, 0.5)'] + ['rgba(220, 235, 245, 0.5)'] * 2),  # Darker color for the first column
                           align='center')
    )])


    # Set the table colors and style
    table.update_layout(
        title = 'My top authors - read books stats',
        template='plotly_white',
        plot_bgcolor='white',
        paper_bgcolor='white',
        width=500,
        height=600
    )

    return table