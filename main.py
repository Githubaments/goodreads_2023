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

    st.write('### Books Read Over Time')
    books_read = data['Date Read'].value_counts().resample('M').sum().dropna()
    st.line_chart(books_read)

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

    st.write('### Average Rating of Books')
    fig = px.bar(data, x=data.index, y='Average Rating', labels={'x': 'Book Index', 'y': 'Average Rating'})
    st.plotly_chart(fig)

    st.write('### Scatter Plot: Length vs. Average Rating')
    fig = px.scatter(data, x='Number of Pages', y='Average Rating', labels={'x': 'Number of Pages', 'y': 'Average Rating'})
    st.plotly_chart(fig)

    st.write('### Scatter Plot: Original Publication Year vs. Average Rating')
    fig = px.scatter(data, x='Original Publication Year', y='Average Rating', labels={'x': 'Original Publication Year', 'y': 'Average Rating'})
    st.plotly_chart(fig)

    st.write('### Gender Analysis of Authors')
    data['Gender'] = data['Author'].apply(get_gender)
    gender_counts = data['Gender'].value_counts()
    st.bar_chart(gender_counts)

else:
    st.warning('Please upload a CSV file.')
