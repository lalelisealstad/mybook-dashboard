
# Import libraries 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from collections import Counter
import numpy as np
import re

# topics viz tree map

def tree_topics(topics_dict): 
    """
    Creates a tree map visualization of book topics by count
    param: dictionary containing title of the book as key and the value is one list containing the book's topics
    """
    word_counts_dict = Counter()

    # Count the occurrences of each word in the values of the original dictionary
    for values in topics_dict.values():
        for value in values:
            for word in value.replace(', ', ',').split(','):
                word_counts_dict[word.lower()] += 1

    df_word_counts = pd.DataFrame(list(word_counts_dict.items()), columns=['Word', 'Count'])
    df_word_counts = df_word_counts.sort_values(by='Count', ascending=False).reset_index().head(45)

    fig = px.treemap(
        df_word_counts,
        path=['Word'],
        values='Count',
        custom_data=['Count'] )

    fig.update_layout(
        title={
            'text': 'Most common book topics',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                size=22
            )
        },
        uniformtext=dict(minsize=16),  # Increase the minimum text size to 70
        font=dict(
            size=16  # Adjust the font size for the entire figure
        )
    )
    
    
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Count: %{customdata[0]}'
    )
    # Show the plot
    return fig


# Publication year and rating 
def viz_pub_year(df):

    # Group the DataFrame by year and calculate the average rating and count of books
    df = df.query('Original_Publication_Year != 0')
    year_data = df.groupby('Original_Publication_Year',  observed=True).agg({'My_Rating': 'mean', 'Title': 'count'}).reset_index()
    
    # Extract the year labels, average ratings, and book counts
    labels = year_data['Original_Publication_Year']
    ratings = year_data['My_Rating']
    book_counts = year_data['Title']
    
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
            colorscale='Purp',  # Choose a desired color scale
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


# Publication year vs rating 
def viz_year_read(df):
    
    df = df.dropna(subset=['Year_Quarter'])
    
    # Count the number of books read in each year and quarter
    year_quarter_counts = df.groupby('Year_Quarter',  observed=True).size().reset_index(name='Books Read')
    
    # Create the line chart
    fig = px.line(year_quarter_counts, x='Year_Quarter', y='Books Read', markers=True, template = "plotly_white")
    fig['data'][0]['line']['color']='#A777F1'
    # Customize the plot layout
    fig.update_layout(
        title='Number of Books Read per Year and Quarter<span style="font-size: 8px;"><br>Using dates read in Goodreads, or date added to Goodreads</span>',
        xaxis=dict(title='Year and Quarter'),
        yaxis=dict(title='Number of Books Read'),
        showlegend=False
    )
    return fig

### Page count 

def visualize_categories(myreads, column, title, xtitle):
    # Group the DataFrame by page category and count the number of books in each category
    category_counts = myreads[column].value_counts().sort_index()

    # Assign a unique color to each category
    colors = ['rgb(251,180,174)', 'rgb(179,205,227)', 'rgb(204,235,197)', 'rgb(222,203,228)', 'rgb(254,217,166)', 'rgb(250,231,175)','rgb(251,180,174)' ]

    # Create the bar chart
    fig = go.Figure(data=go.Bar(
        x=category_counts.index,
        y=category_counts.values,
        marker=dict(color=colors),
    ))

    # Set the chart title and axis labels
    fig.update_layout(
        title=title,
        xaxis=dict(title=xtitle),
        yaxis=dict(title='Number of Books'),
        template = "plotly_white"
    )
    
    return fig


# pie chart, top 5 categories and languages

def viz_top_values(column, top_n=5):
    # Drop NaN values from the column
    column = column.dropna()
    value_col = column.value_counts().reset_index()

    if len(value_col) > top_n: 
        remaining_count =value_col['count'].iloc[top_n:].sum()
        other = pd.DataFrame([['Other', remaining_count]], columns=[value_col.columns[0], 'count'])
        val_df =  pd.DataFrame(pd.concat([value_col.head(top_n), other]))
    else:
        val_df = pd.DataFrame(value_col)


    labels = val_df.iloc[:, 0]
    values = val_df['count']

    # Define the color theme
    colors = ['rgb(179,205,227)', 'rgb(204,235,197)', 'rgb(222,203,228)', 'rgb(254,217,166)', 'rgb(250,231,175)','rgb(251,180,174)', 'rgb(251,180,174)','#9DC8C8', '#84B1ED' ]

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # Set the colors using the color theme
    fig.update_traces(marker=dict(colors=colors))

    fig.update_layout(title=f'Top {top_n} {column.name}')

    return fig


#### highest and lowest rated books

def book_ratings_top(data, title_txt):
    # Define custom colors
    my_rating_color = 'rgb(180,151,231)'
    google_books_color = '#34A853'
    goodreads_color = '#e9e5cd'

    # Filter the data where My_Rating > 0 since this would include non-rated books
    filtered_data = data[data['My_Rating'] > 0]

    # Sort the filtered data by your own rating in ascending order for bottom-rated books
    filtered_data = filtered_data.sort_values(['My_Rating', 'Date_Read'], ascending=True)

    # Select the top 10 books based on your own rating
    top_books = filtered_data.tail(15)

    # Create the figure object
    fig = px.scatter(template = "plotly_white")

    # Add trace for Average_Rating_GoogleBooks as dots with a different color and shape
    fig.add_trace(go.Scatter(
        x=top_books['Average_Rating_GoogleBooks'],
        y=top_books['Title'],
        mode='markers',
        name=f"Average Rating Google Books",
        marker=dict(color=google_books_color, symbol='square', size=15),
    ))

    # Add trace for Average_Rating_Goodreads as dots with a different color and shape
    fig.add_trace(go.Scatter(
        x=top_books['Average_Rating_Goodreads'],
        y=top_books['Title'],
        mode='markers',
        name='Average Rating Goodreads',
        marker=dict(color=goodreads_color, symbol='diamond', size=15),
    ))

    # Add trace for My Rating as dots
    fig.add_trace(go.Scatter(
        x=top_books['My_Rating'],
        y=top_books['Title'],
        mode='markers',
        name='My Rating',
        marker=dict(color=my_rating_color, symbol='circle', size=15),
    ))

    # Update the layout
    fig.update_layout(
        title= f'{title_txt}<br><span style="font-size: 11px;">*Showing only 15 latest read books</span>',
        # font=dict(size=12),
        yaxis=dict(title='Title', side='top', showticklabels=True),
        xaxis=dict(
            title='Rating',
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            range=[0.5, 5.5],  # Set the X-axis range from 0 to 5, 
            showgrid=True),
        legend=dict(
            title='Rating',  # Set legend title
            orientation='h',  # Set legend orientation (horizontal)
            x=0.01,  # Adjust x position of the legend
            y=1.2,  # Adjust y position of the legend
        )
        )
    return fig


def book_ratings_bottom(data, title_txt):
    # Define custom colors
    my_rating_color = 'rgb(180,151,231)'
    google_books_color = '#34A853'
    goodreads_color = '#e9e5cd'

    # Filter the data where My_Rating > 0 since this would include non-rated books
    filtered_data = data[data['My_Rating'] > 0]

    # Sort the filtered data by your own rating in ascending order for bottom-rated books
    filtered_data = filtered_data.sort_values(['My_Rating', 'Date_Read'], ascending=True)

    # Select the top 10 books based on your own rating
    top_books = filtered_data.head(15)

    # Create the figure object
    fig = px.scatter(template = "plotly_white")

    # Add trace for My Rating as dots
    fig.add_trace(go.Scatter(
        x=top_books['My_Rating'],
        y=top_books['Title'],
        mode='markers',
        name='My Rating',
        marker=dict(color=my_rating_color, symbol='circle', size=15),
    ))

    # Add trace for Average_Rating_GoogleBooks as dots with a different color and shape
    fig.add_trace(go.Scatter(
        x=top_books['Average_Rating_GoogleBooks'],
        y=top_books['Title'],
        mode='markers',
        name=f"Average Rating Google Books",
        marker=dict(color=google_books_color, symbol='square', size=15),
    ))

    # Add trace for Average_Rating_Goodreads as dots with a different color and shape
    fig.add_trace(go.Scatter(
        x=top_books['Average_Rating_Goodreads'],
        y=top_books['Title'],
        mode='markers',
        name='Average Rating Goodreads',
        marker=dict(color=goodreads_color, symbol='diamond', size=15),
    ))

    # Update the layout
    fig.update_layout(
        title= f'{title_txt}<br><span style="font-size: 11px;">*Showing only 15 latest read books</span>',
        # font=dict(size=12),
        yaxis=dict(title='Title', side='top', showticklabels=True),
        xaxis=dict(
            title='Rating',
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            range=[0.5, 5.5],  # Set the X-axis range from 0 to 5, 
            showgrid=True),
        legend=dict(
            title='Rating',  # Set legend title
            orientation='h',  # Set legend orientation (horizontal)
            x=0.01,  # Adjust x position of the legend
            y=1.2,  # Adjust y position of the legend
        )
        )
    return fig




# Rating comparison table 

def create_rating_table(data):
    # Filter the data where My_Rating > 0
    filtered_data = data[data['My_Rating'] > 0]

    # Calculate the mean ratings
    mean_ratings = filtered_data[['Average_Rating_GoogleBooks', 'Average_Rating_Goodreads', 'My_Rating']].mean()

    # Create a list of rating names
    ratings = ['My Ratings - Average', 'Ratings (Google Books) - Average', 'Ratings (Goodreads) - Average']

    # Create a list of mean rating values
    mean_values = np.round(mean_ratings.values.tolist(),2)

    # Create a Plotly table
    table = go.Figure(data=[go.Table(
        header=dict(values=['Rating', 'Mean Rating'],
                    fill_color='rgba(230,230,250, 1)',
                    align=['left', 'center']),
        cells=dict(values=[ratings, mean_values],
                   fill_color='rgba(248,248,255,0.5)',
                   align=['left', 'center'])
    )])

    # Set the table colors
    table.update_layout(
        title = 'My rating vs other people ratings',
        template='plotly_white',
        plot_bgcolor='white'
    )

    return table



# My top authors 

def create_author_table(data):
    # Filter the data to include only the books you've read
    data = data[data['Author'].isin(data['Author'].value_counts().nlargest(5).index)].copy()

    # Replace 0 by np.nan so its not included in the mean (Usally 0 rating means it is not rated) 
    data['My_Rating'] = data['My_Rating'].replace(0, np.nan)

    # Calculate the mean 'My_Rating' grouped by 'Author'
    data['mean_rating_by_author'] = data.groupby('Author',  observed=True)['My_Rating'].transform('mean').copy()

    data['My_Rating'] = np.where((data['My_Rating'] == np.nan) | data['My_Rating'].isnull(), data['mean_rating_by_author'], data['My_Rating'])

    # Group the data by author and calculate the required statistics
    author_stats = np.round(data.groupby('Author',  observed=True).agg({
        'Read_Count' :'count', 
        'My_Rating': 'mean',
        'Average_Rating_Goodreads': 'mean',
        'Rating_Count': 'sum',
    }).reset_index(),1)

    # Sort the authors based on the mean rating in descending order
    sorted_authors = author_stats.sort_values('Read_Count', ascending=False)

    # Select the top five authors
    top_authors = sorted_authors.head(5)

    # Create a Plotly table
    table = go.Figure(data=[go.Table(
        header=dict(values=['Author', 'Read count', 'My Average Rating'], #, 'Number of times rated on Goodreads', 'Average Goodreads Rating'],
                    fill_color='rgba(230,230,250, 1)',
                    align='center'),
        cells=dict(values=[top_authors['Author'],
                           top_authors['Read_Count'],
                           top_authors['My_Rating']],
                        #    top_authors['Rating_Count'],
                        #    top_authors['Average_Rating_Goodreads']], 
                           fill=dict(color=['rgba(230,230,250, 0.5)'] + ['rgba(248,248,255,0.5)'] * 2),  # Darker color for the first column
                           align='center')
    )])


    # Set the table colors and style
    table.update_layout(
        title = 'My most read authors',
        template='plotly_white',
        plot_bgcolor='white',
        paper_bgcolor='white',
        # font=dict(size=12),  
    )

    return table


# Three viz of count of words in description

def desc_tree(Description):
    from collections import Counter
    stopwords_dict = {'like', 'author', 'S', 'will','new','york','time','book','novel', 'read', 'day', 'make','year', 'one', 'times', 'times, of', 's', 'award','author','new','york','selling','story','t','1','og', 'call', 'upon', 'still', 'nevertheless', 'down', 'every', 'forty', '‘re', 'always', 'whole', 'side', "n't", 'now', 'however', 'an', 'show', 'least', 'give', 'below', 'did', 'sometimes', 'which', "'s", 'nowhere', 'per', 'hereupon', 'yours', 'she', 'moreover', 'eight', 'somewhere', 'within', 'whereby', 'few', 'has', 'so', 'have', 'for', 'noone', 'top', 'were', 'those', 'thence', 'eleven', 'after', 'no', '’ll', 'others', 'ourselves', 'themselves', 'though', 'that', 'nor', 'just', '’s', 'before', 'had', 'toward', 'another', 'should', 'herself', 'and', 'these', 'such', 'elsewhere', 'further', 'next', 'indeed', 'bottom', 'anyone', 'his', 'each', 'then', 'both', 'became', 'third', 'whom', '‘ve', 'mine', 'take', 'many', 'anywhere', 'to', 'well', 'thereafter', 'besides', 'almost', 'front', 'fifteen', 'towards', 'none', 'be', 'herein', 'two', 'using', 'whatever', 'please', 'perhaps', 'full', 'ca', 'we', 'latterly', 'here', 'therefore', 'us', 'how', 'was', 'made', 'the', 'or', 'may', '’re', 'namely', "'ve", 'anyway', 'amongst', 'used', 'ever', 'of', 'there', 'than', 'why', 'really', 'whither', 'in', 'only', 'wherein', 'last', 'under', 'own', 'therein', 'go', 'seems', '‘m', 'wherever', 'either', 'someone', 'up', 'doing', 'on', 'rather', 'ours', 'again', 'same', 'over', '‘s', 'latter', 'during', 'done', "'re", 'put', "'m", 'much', 'neither', 'among', 'seemed', 'into', 'once', 'my', 'otherwise', 'part', 'everywhere', 'never', 'myself', 'must', 'will', 'am', 'can', 'else', 'although', 'as', 'beyond', 'are', 'too', 'becomes', 'does', 'a', 'everyone', 'but', 'some', 'regarding', '‘ll', 'against', 'throughout', 'yourselves', 'him', "'d", 'it', 'himself', 'whether', 'move', '’m', 'hereafter', 're', 'while', 'whoever', 'your', 'first', 'amount', 'twelve', 'serious', 'other', 'any', 'off', 'seeming', 'four', 'itself', 'nothing', 'beforehand', 'make', 'out', 'very', 'already', 'various', 'until', 'hers', 'they', 'not', 'them', 'where', 'would', 'since', 'everything', 'at', 'together', 'yet', 'more', 'six', 'back', 'with', 'thereupon', 'becoming', 'around', 'due', 'keep', 'somehow', 'n‘t', 'across', 'all', 'when', 'i', 'empty', 'nine', 'five', 'get', 'see', 'been', 'name', 'between', 'hence', 'ten', 'several', 'from', 'whereupon', 'through', 'hereby', "'ll", 'alone', 'something', 'formerly', 'without', 'above', 'onto', 'except', 'enough', 'become', 'behind', '’d', 'its', 'most', 'n’t', 'might', 'whereas', 'anything', 'if', 'her', 'via', 'fifty', 'is', 'thereby', 'twenty', 'often', 'whereafter', 'their', 'also', 'anyhow', 'cannot', 'our', 'could', 'because', 'who', 'beside', 'by', 'whence', 'being', 'meanwhile', 'this', 'afterwards', 'whenever', 'mostly', 'what', 'one', 'nobody', 'seem', 'less', 'do', '‘d', 'say', 'thus', 'unless', 'along', 'yourself', 'former', 'thru', 'he', 'hundred', 'three', 'sixty', 'me', 'sometime', 'whose', 'you', 'quite', '’ve', 'about', 'even'}
        
    descriptions_all = ' '.join(Description.dropna()).lower()

    descriptions_all = re.findall(r'\b\w+\b', descriptions_all.lower())

    # Remove stop words from the list of words
    filtered_words = [word for word in descriptions_all if word not in stopwords_dict]

    word_counts = Counter(filtered_words)

    # Create a DataFrame from the word counts
    word_counts_df = pd.DataFrame(word_counts.items(), columns=['Word', 'Count'])
    # Create a tree map using Plotly Express
    fig = px.treemap(word_counts_df.sort_values(by='Count', ascending=False).head(55), path=['Word'], values='Count', custom_data=['Count'] )

    fig.update_layout(
        title={
            'text': 'Most common words found in book descriptions',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            # 'font': dict(
            #     size=22
            # )
        },
        # uniformtext=dict(minsize=16),  # Increase the minimum text size to 70
        # font=dict(
        #     size=16  # Adjust the font size for the entire figure
        # )
    )

    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Count: %{customdata[0]}'
    )

    return fig


import plotly.express as px
import plotly.graph_objects as go

def scatter_popularity(df):
    # Create scatter plot

    df['My_Rating'] = df['My_Rating'].replace(0, np.nan)
    df = df.dropna(subset=['Rating_Count', 'Average_Rating_Goodreads'])

    melted_df = pd.melt(df[['Rating_Count', 'Average_Rating_Goodreads', 'My_Rating']], id_vars=['Rating_Count'], value_vars=['Average_Rating_Goodreads', 'My_Rating'],
                        var_name='Rating_Type', value_name='Rating')

    color_scale = px.colors.qualitative.Set2[2:8]  # 

    fig = px.scatter(
        melted_df, x='Rating_Count', y='Rating',color='Rating_Type', trendline="ols", title="Does popularity correlate with rating?<br>",
        template="plotly_white",  
        color_discrete_sequence=color_scale, 
        labels={"Rating_Type": "Rating", 'Average_Rating_Goodreads': "Average Rating on Goodreads"},
        category_orders={"Rating_Type": ["Average_Rating_Goodreads", "My_Rating"]}
    )
    # Customize the legend
    fig.update_layout(
        legend=dict(
            title='Rating Type:', 
            orientation='h',  
            x=0.5,  
            y=1.2,  
        ),
        
        xaxis=dict(
            title='Number of times the book has been rated in Google Books',  
        ),
        
        yaxis=dict(
            title='Rating', 
        )
    )
    return fig


## Genre lollipopp

def lolli_fig(tbl_genre):

    fig = px.scatter(tbl_genre, 
        x=tbl_genre.index.tolist(), 
        y="My_Rating",
        size="genres", 
        color=tbl_genre.index.tolist(),
        size_max=50, 
        )
    fig.update_traces(hovertemplate='Genre: %{x} <br>My average rating of books with genre: %{y}<br>Number of read books with genre: %{marker.size:}') #
    
    fig2 = px.bar(x=tbl_genre.index, y=tbl_genre['My_Rating'])
    
    fig2.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(158,202,225)',
                    marker_line_width=1.5, opacity=0.9, width=0.1)                  

    fig3 = go.Figure(data=fig.data + fig2.data)
    
    fig3.update_layout(
        title={
            'text': 'My average rating and Number of books read with genre',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis_range=[1,5],
        template="plotly_white",  
        showlegend = False, 
        )
    
    fig3.add_annotation(
        x=0.5,
        y=1.11,
        xref='paper',
        yref='paper',
        text="The size of the bubble represent the number of books read within genre. <br> The position of the bubble along the y-axis represent how well books within the genre have been rated.",
        showarrow=False,
        # font=dict(size=10),
    )
        
    return fig3
 
 
# Spider figure - genre rating     
    
import plotly.express as px

def spider_fig(tbl_genre):
    spider_fig = px.line_polar(tbl_genre, r=tbl_genre.My_Rating, theta=tbl_genre.index, line_close=True, range_r=[1, tbl_genre.My_Rating.max()+0.2]).update_traces(fill='tonext', fillcolor='rgba(167, 119, 241, 0.5)')
    spider_fig.update_layout(template='plotly_white')
    return spider_fig
    
    
    
# Genre - year quarter timeline

import plotly.express as px

def stack_fig(allgenredf, tbl_genre):
    
    tbl_percent = (
        pd.DataFrame(
            allgenredf.query('Read_Count > 0 & genres in @tbl_genre.index.tolist()')
            .groupby('Year_Quarter',observed=True)['genres'].value_counts(normalize = True)
            )
        .reset_index()
        .query('Year_Quarter != "" and proportion > 0.01')
    )
    
    fig = px.area(tbl_percent, x='Year_Quarter',y='proportion', color='genres', line_group='genres',
                title='Do I go through periods were I read more of the same genres?<span style="font-size: 10px;"><br>Figure shows the proportion of books in each genre read in that year-quarter. A book can have multiple genres.</span>')
        
    fig.update_layout( 
        xaxis_title='Year quarter',
        yaxis_title='Proportion of books read with genre',
        legend_title="Genre",
        template="plotly_white")

    return fig 