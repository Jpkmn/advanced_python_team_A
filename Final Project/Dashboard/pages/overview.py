# overview.py
import streamlit as st
import pandas as pd

# Method to show the overview page
def show_page():
    st.title("Airline Customer Satisfaction Dashboard")

    st.header("Welcome to the Airline Customer Satisfaction Dashboard!")
    st.write("""
        This dashboard provides an in-depth analysis of airline customer satisfaction data.
        It includes several subpages that can be accessed from the sidebar on the left:
        - **Overview**: Introduction to the dashboard and the data.
        - **Detailed Analysis**: Visualizations and analysis of customer satisfaction and related features.
        - **Predict Satisfaction**: Predict the satisfaction of individual customers based on input features.
        - **Batch Prediction**: Upload an Excel file to predict the satisfaction of multiple customers at once.
        - **Feature Importance**: Display the importance of different features in the XGBoost model used for prediction.
    """)
    st.subheader("Dataset")
    df = pd.read_csv('./data/Airline_customer_satisfaction.csv')
    st.write("Below is the data used in this dashboard and for model training (XGBoost):")
    st.dataframe(df)
    # Display the number of rows and columns
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")

# Display the content
if __name__ == "__main__":
    show_page()