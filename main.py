import streamlit as st
import pandas as pd
import numpy as np
import gender_guesser.detector as gender

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
    st.write(f"Average rating: {data['Average Rating'].mean():.2f}")

    st.write('### Average Length of Books')
    st.write(f"Average number of pages: {data['Number of Pages'].mean():.0f}")

    st.write('### Average Original Publication Year')
    st.write(f"Average original publication year: {data['Original Publication Year'].mean():.0f}")

    st.write('### Gender Analysis of Authors')
    data['Gender'] = data['Author'].apply(get_gender)
    gender_counts = data['Gender'].value_counts()
    st.bar_chart(gender_counts)

else:
    st.warning('Please upload a CSV file.')
