import streamlit as st
import pandas as pd
import numpy as np
import gender_guesser.detector as gender
import plotly.express as px

# Load data
def load_data(file):
    data = pd.read_csv(file, parse_dates=['Date Read', 'Date Added'])
    return data

def get_gender(name):
    d = gender.Detector()
    first_name = name.split()[0]
    return d.get_gender(first_name)

st.title('Goodreads Book Analysis')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = load_data(uploaded_file)

    st.write('### Cumulative Books Read Over Time')
    books_read = data['Date Read'].value_counts().resample('M').sum().dropna()
    cumulative_books_read = books_read.cumsum()
    fig = px.line(x=cumulative_books_read.index, y=cumulative_books_read, labels={'x': 'Date', 'y': 'Cumulative Books Read'})
    st.plotly_chart(fig)

    st.write('### Top Authors')
    top_authors = data['Author'].value_counts().head(10)
    st.bar_chart(top_authors)

    st.write('### Average Rating by Year')
    data['Year Read'] = data['Date Read'].dt.year
    avg_ratings_by_year = data.groupby('Year Read')['My Rating'].mean().dropna()
    st.line_chart(avg_ratings_by_year)

    st.write('### Distribution of Ratings')
    ratings_count = data['My Rating'].value_counts().sort_index()
    st.bar_chart(ratings_count)

    st.write('### Scatter Plot: Length vs. Average Rating')
    fig = px.scatter(data, x='Number of Pages', y='Average Rating', hover_name='Title', labels={'x': 'Number of Pages', 'y': 'Average Rating'})
    st.plotly_chart(fig)

    st.write('### Scatter Plot: Original Publication Year (since 1500) vs. Average Rating')
    data_since_1500 = data[data['Original Publication Year'] >= 1500]
    fig = px.scatter(data_since_1500, x='Original Publication Year', y='Average Rating', hover_name='Title', labels={'x': 'Original Publication Year', 'y': 'Average Rating'})
    st.plotly_chart(fig)

    st.write('### Scatter Plot: Original Publication Year (Since 1900) vs. Average Rating')
    data_last_100_years = data[data['Original Publication Year'] >= 1900]
    fig = px.scatter(data_last_100_years, x='Original Publication Year', y='Average Rating', hover_name='Title', labels={'x': 'Original Publication Year', 'y': 'Average Rating'}, size=data_last_100_years.groupby(['Original Publication Year', 'Average Rating']).transform('count'))
    st.plotly_chart(fig)

    st.write('### Scatter Plot: Original Publication Year (Since 2000) vs. Average Rating')
    data_last_20_years = data[data['Original Publication Year'] >= 2000]
    fig = px.scatter(data_last_20_years, x='Original Publication Year', y='Average Rating', hover_name='Title', labels={'x': 'Original Publication Year', 'y': 'Average Rating'}, size=data_last_20_years.groupby(['Original Publication Year', 'Average Rating']).transform('count'))
    st.plotly_chart(fig)
    
    
    st.write('### Gender Analysis of Authors (Percentage)')
    data['Gender'] = data['Author'].apply(get_gender)
    gender_counts = data['Gender'].value_counts()

    # Combine gender categories
    male_count = gender_counts['male'] + gender_counts['mostly_male']
    female_count = gender_counts['female'] + gender_counts['mostly_female']
    unknown_count = gender_counts['andy'] + gender_counts['unknown']
    combined_gender_counts = pd.Series([male_count, female_count, unknown_count], index=['Male', 'Female', 'Unknown'])

    # Calculate percentages
    gender_percentage = (combined_gender_counts / combined_gender_counts.sum()) * 100
    fig = px.bar(gender_percentage, x=gender_percentage.index, y=gender_percentage, labels={'x': 'Gender', 'y': 'Percentage'})
    st.plotly_chart(fig)

else:
    st.warning('Please upload a CSV file.')
