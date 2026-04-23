import streamlit as st
import pandas as pd
import plotly.express as px
from login import login_user, register_user

st.title("Local Tourism Promotion Portal")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

required_columns = ['Year', 'Month', 'Location', 'Visitors', 'Revenue']

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if choice == "Register":
    st.subheader("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Register"):
        register_user(username, password)
        st.success("Registration Successful!")

elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        result = login_user(username, password)

        if result:
            st.session_state.logged_in = True
            st.success(f"Welcome {username}")
        else:
            st.error("Invalid Credentials")

    if st.session_state.logged_in:

        st.subheader("Required Dataset Format")
        sample_df = pd.DataFrame({
            "Year": [2025],
            "Month": ["January"],
            "Location": ["Manali"],
            "Visitors": [1700],
            "Revenue": [85000]
        })
        st.dataframe(sample_df)

        uploaded_file = st.file_uploader("Upload Tourism Dataset CSV", type=["csv"])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)

            if all(col in df.columns for col in required_columns):

                st.success("Dataset uploaded successfully")
                st.dataframe(df)

                st.subheader("Visitors by Location")
                fig1 = px.bar(df, x='Location', y='Visitors', color='Location')
                st.plotly_chart(fig1)

                st.subheader("Revenue Trend")
                fig2 = px.histogram(df, x='Month', y='Revenue', color='Location')
                st.plotly_chart(fig2)

                st.subheader("Best Location by Month")
                best_location = df.loc[df.groupby("Month")["Visitors"].idxmax()][["Month", "Location", "Visitors"]]
                st.dataframe(best_location)
                
                st.subheader("Visitors Trend by Year")
                fig3 = px.line(df, x='Year', y='Visitors', color='Location', markers=True)
                st.plotly_chart(fig3)

                st.subheader("Revenue Trend by Year")
                fig4 = px.box(df, x='Year', y='Revenue', color='Location')
                st.plotly_chart(fig4)

                best_overall = df.groupby("Location")["Visitors"].sum().idxmax()
                st.success(f"Best Overall Tourist Destination: {best_overall}")
                
            else:
                st.error("Invalid dataset format.")
                st.write("Required columns:", required_columns)
