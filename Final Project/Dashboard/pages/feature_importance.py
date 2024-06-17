# feature_importance.py
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# Method to show the feature importance page
def show_page():
    st.title("Feature Importance")

    st.header("Importance of Features in the XGBoost Model")

    st.write("The feature importance values represent the relative importance of each feature in predicting "
             "customer satisfaction. It helps understand which features have the most impact on the model's predictions. "
             "Thus, airlines can focus on improving these key features to enhance customer satisfaction.")

    # Load the model and extract feature importances
    model = joblib.load('./pages/xgboost.pkl')
    feature_importances = model.named_steps['classifier'].feature_importances_

    categorical_features = ['Customer Type', 'Class', 'Type of Travel']
    numerical_features = ['Age', 'Flight Distance', 'Seat comfort', 'Food and drink',
                          'Inflight wifi service', 'Inflight entertainment', 'Online support',
                          'Ease of Online booking', 'On-board service', 'Leg room service',
                          'Baggage handling', 'Checkin service', 'Cleanliness', 'Online boarding',
                          'Departure Delay in Minutes', 'Arrival Delay in Minutes']

    feature_names = model.named_steps['preprocessor'].transformers_[0][1].named_steps['ohe'].get_feature_names_out(categorical_features).tolist() + numerical_features
    importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
    importance_df = importance_df.sort_values(by='Importance', ascending=True)

    # Display feature importance in a horizontal bar chart
    fig = px.bar(importance_df, x='Importance', y='Feature', orientation='h', title='Feature Importance')
    st.plotly_chart(fig)

    # Display the top 3 most important features
    st.subheader("Feature Importance Results")
    st.write("The top 3 most important features airlines should focus on to improve customer satisfaction are:")
    st.write(f"Inflight entertainment: 0.41/1.0")
    st.write(f"Seat comfort: 0.12/1.0")
    st.write(f"Ease of online booking: 0.06/1.0")

if __name__ == "__main__":
    show_page()