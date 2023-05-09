import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import time

import mysql.connector as connection

joy = connection.connect(host='relational.fit.cvut.cz', database = 'university',user = 'guest', passwd='relational',use_pure=True)

registration_df = pd.read_sql_query('select * from registration',joy)

from PIL import Image
logo = Image.open("logo.png")
st.set_page_config(page_title='Registration Portal', page_icon=logo)
custom_primary_color = '#8b5e83'
custom_secondary_color = '#ffeecf'

footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f5f5f5;
    color: #333;
    text-align: center;
    padding: 10px;
    font-size: 16px;
}
</style>
<div class="footer">
<p>© 2023 CTU University</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

# Add a slider and display its value
age = st.slider("What is your age?", 18, 100)
st.markdown(f"<p>You selected: <strong>{age}</strong></p>", unsafe_allow_html=True)


COLOR = 'purple'


# Add custom CSS
st.markdown("""
<style>
    /* Import the font from Google Fonts */
    @import url('https://fonts.googleapis.com/css?family=Montserrat');
    
    /* Use the font in the app */
    body {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Change the color of the button */
    .stButton button {
        background-color: #8b5e83 !important;
        color: white !important;
    }
    
    /* Add some padding to the sidebar */
    .sidebar .sidebar-content {
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)



# Add a styled header with emojis
st.markdown("<h1 style='text-align: center;'>🚀 Welcome to the CTU University Registration App 🎓</h1>", unsafe_allow_html=True)

# Add some styled text with an emoji
st.markdown(f"<p style='color: {custom_secondary_color};'>Click the button below to register now! 👇</p>", unsafe_allow_html=True)

# Add a styled button with an emoji
st.button("👉 Register now 👈")

# Add a progress bar
with st.spinner('Loading data...'):
    for i in range(100):
        time.sleep(0.05)
        st.progress(i + 1)
st.success('Data loaded!')


option = st.selectbox('Select an option', ['Option 1', 'Option 2', 'Option 3', 'option 4', 'Option 5', 'Option 6', 'Option 7'])




# Add some styled text
st.markdown(f"<p style='color: {custom_secondary_color};'>Welcome to the CTU University Registration App! Use the sidebar to filter and explore registration data.</p>", unsafe_allow_html=True)

# Add a styled button
st.markdown(f"<button style='background-color: {custom_primary_color}; color: white; border-radius: 5px; padding: 10px;'>Click me!</button>", unsafe_allow_html=True)

footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f5f5f5;
    color: #333;
    text-align: center;
    padding: 10px;
    font-size: 16px;
}
</style>
<div class="footer">
<p>© 2023 CTU University</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

value = st.slider('Select a value', 0, 100, 50)


st.markdown("""
<style>
    /* Import the font from Google Fonts */
    @import url('https://fonts.googleapis.com/css?family=Montserrat');
    
    /* Use the font in the app */
    body {
        font-family: 'Montserrat', sans-serif;
    }
</style>
""", unsafe_allow_html=True)









                        




st.markdown("""
<style>
body {
background-color: #F0F0F0;
font_size: 16px;
}
</style>
""",
            unsafe_allow_html=True
           )

st.markdown(
    """
    <style>
    /* Add custom styles here */
    </style>
    """,
    unsafe_allow_html=True
)


# Add a search bar to allow users to search for a specific student or course by name
search_term = st.sidebar.text_input("Search for a student or course")
if search_term:
    filtered_data = registration_df['registration'.apply(lambda row: search_term.lower() in row.astype(int).str.lower().any(), axis=1)]
else:
    filtered_data = registration_df
    
    

# Display the registration data in a Streamlit table
st.dataframe(filtered_data)

# Create a dropdown menu of all the available courses
courses = sorted(filtered_data['course_id'].unique())
selected_course = st.sidebar.selectbox("Select a course", courses)

# Filter the data to only include the selected course
course_data = filtered_data[filtered_data['course_id'] == selected_course]

# Display a summary of the grades and SAT scores for the selected course
mean_grade = course_data['grade'].mean()
mean_sat = course_data['sat'].mean()

st.write(f"Mean grade for {selected_course}: {mean_grade:.2f}")
st.write(f"Mean SAT score for {selected_course}: {mean_sat:.2f}")

# Create a scatter plot that shows the relationship between grades and SAT scores for each course
scatter_data = filtered_data.groupby(['course_id', 'student_id']).agg({'grade': 'mean', 'sat': 'mean'}).reset_index()

fig = px.scatter(scatter_data, x="sat", y="grade", color="course_id", hover_data=["student_id"])
st.plotly_chart(fig)

# Implement a machine learning model to predict a student's grade based on their SAT score
st.sidebar.write("Predict a student's grade based on their SAT score")

# Create a dropdown menu of all the available students
students = sorted(filtered_data['student_id'].unique())
selected_student = st.sidebar.selectbox("Select a student", students)

# Filter the data to only include the selected student
student_data = filtered_data[filtered_data['student_id'] == selected_student]

# Train a linear regression model on the student's grades and SAT scores
X = student_data['sat'].values.reshape(-1, 1)
y = student_data['grade'].values.reshape(-1, 1)
regressor = LinearRegression()
regressor.fit(X, y)

# Display the predicted grade for the student
sat_input = st.sidebar.number_input("Enter the student's SAT score", value=mean_sat)
predicted_grade = regressor.predict([[sat_input]])[0][0]

st.sidebar.write(f"Predicted grade for {selected_student}: {predicted_grade:.2f}")

# Use Streamlit's interactive widgets to allow users to filter the data based on various criteria
st.sidebar.write("Filter the data")
min_grade, max_grade = st.sidebar.slider("Select a grade range", min_value=0, max_value=100, value=(0, 100))

st.markdown("""
---
© 2023 CTU University. All rights reserved.
| [Privacy policy](https://ctu.edu/privacy)
| [Terms of service](https://ctu.edu/terms)
""")


