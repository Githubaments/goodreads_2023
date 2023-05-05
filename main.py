# ... (rest of the imports and functions)

st.title('Goodreads Book Analysis')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = load_data(uploaded_file)

    # ... (rest of the code)

    st.write('### Scatter Plot: Length vs. Average Rating')
    fig = px.scatter(data, x='Number of Pages', y='Average Rating', hover_name='Title', labels={'x': 'Number of Pages', 'y': 'Average Rating'})
    st.plotly_chart(fig)

    st.write('### Scatter Plot: Original Publication Year (since 1500) vs. Average Rating')
    data_since_1500 = data[data['Original Publication Year'] >= 1500]
    fig = px.scatter(data_since_1500, x='Original Publication Year', y='Average Rating', hover_name='Title', labels={'x': 'Original Publication Year', 'y': 'Average Rating'})
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
