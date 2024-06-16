# app.py
import streamlit as st
from st_pages import Page, show_pages, add_page_title

# Declare the pages in the app
show_pages(
    [
        Page("pages/overview.py", "Overview", "🏠"),
        Page("pages/detailed_analysis.py", "Detailed Analysis", ":bar_chart:"),
        Page("pages/predict_satisfaction.py", "Predict Satisfaction", "🔍"),
        Page("pages/batch_prediction.py", "Batch Prediction", "📂"),
        Page("pages/feature_importance.py", "Feature Importance", "🔑")
    ]
)

add_page_title()

# Redirect to the "Overview" page on initial load
if "page" not in st.session_state:
    st.session_state.page = "Overview"

st.rerun()