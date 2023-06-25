
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