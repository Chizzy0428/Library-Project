import pandas as pd
import numpy as np
import pickle
import streamlit as st
import random

# Load Pickle Files
with open("df.pkl", "rb") as file:
    df = pickle.load(file)  # Book Dataset

with open("tfidf_model.pkl", "rb") as file:
    tfidf = pickle.load(file)

with open("cosine_sim.pkl", "rb") as file:
    cosine_sim = pickle.load(file)

# Function to get book recommendations
def get_recommendations(title, num_recommendations=5):
    if title not in df['Title of Book'].values:
        return ["Book not found in the database."]
    idx = df[df['Title of Book'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]
    book_indices = [i[0] for i in sim_scores]
    return df['Title of Book'].iloc[book_indices].tolist()

# Function for Chatbot Response
def chatbot_response(user_input):
    department_keywords = {
        'Accounting': 'Accounting',
        'Business': 'Business Administration',
        'Marketing': 'Marketing',
        'Economics': 'condaEconomics',
        'Entrepreneur': 'Entrepreneur',
        'GST': 'Gst',
        'Political': 'Political Science',
        'Mass': 'Mass Communication',
        'Computer': 'Computer Science',
        'Information': 'Information Technology',
        'Software': 'Software Engineering',
        'Pub': 'Pub. Admin',
        'Novel': 'Novel'
    }
    response = "Sorry, I couldn't find any book for your request."
    for keyword, dept in department_keywords.items():
        if keyword.lower() in user_input.lower():
            filtered_books = df[df['Department'] == dept]['Title of Book'].tolist()
            if filtered_books:
                response = f"Here are some {dept} books: {random.sample(filtered_books, min(5, len(filtered_books)))}"
            break
    return response

# Streamlit App
st.sidebar.title("Library System")
page = st.sidebar.selectbox("Choose Page", ["Book Recommendation", "Chatbot"])

if page == "Book Recommendation":
    st.title("Library Book Recommendation System")
    book_title = st.text_input("Enter Book Title")
    if st.button("Recommend"):
        if book_title:
            recommendations = get_recommendations(book_title)
            if "Book not found in the database." in recommendations:
                st.write(recommendations[0])
            else:
                st.write("Recommended Books:")
                for rec in recommendations:
                    st.write(f"- {rec}")
        else:
            st.write("Please enter a book title.")

elif page == "Chatbot":
    st.title("Library Chatbot")
    user_input = st.text_input("Ask for book suggestions by department")
    if st.button("Get Suggestion"):
        if user_input:
            response = chatbot_response(user_input)
            st.write(response)
        else:
            st.write("Please enter your request.")
