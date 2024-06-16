# predict_satisfaction.py
import streamlit as st
import pandas as pd
import joblib

# Method to show the prediction page
def show_page():
    st.title("Predict Customer Satisfaction")

    st.header("Input features for prediction")

    st.write("This page allows you to predict the satisfaction of an individual customer based on the input features "
             "provided. The model used for prediction is an XGBoost trained on airline customer data."
             "It helps to identify the factors that influence customer satisfaction and make recommendations to improve "
             "it.")

    # Read the data and load the model
    df = pd.read_csv('./data/Airline_customer_satisfaction.csv')
    model = joblib.load('./pages/xgboost.pkl')

    # Input form for user to enter data
    customer_type = st.selectbox("Customer Type", options=df["Customer Type"].unique())
    travel_type = st.selectbox("Type of Travel", options=df["Type of Travel"].unique())
    travel_class = st.selectbox("Class", options=df["Class"].unique())
    age = st.number_input("Age", min_value=1, max_value=100, value=30)
    flight_distance = st.number_input("Flight Distance", min_value=1, max_value=10000, value=500)
    seat_comfort = st.slider("Seat comfort", min_value=0, max_value=5, value=3)
    food_drink = st.slider("Food and drink", min_value=0, max_value=5, value=3)
    inflight_wifi_service = st.slider("Inflight wifi service", min_value=0, max_value=5, value=3)
    inflight_entertainment = st.slider("Inflight entertainment", min_value=0, max_value=5, value=3)
    online_support = st.slider("Online support", min_value=0, max_value=5, value=3)
    online_booking = st.slider("Ease of Online booking", min_value=0, max_value=5, value=3)
    onboard_service = st.slider("On-board service", min_value=0, max_value=5, value=3)
    leg_room_service = st.slider("Leg room service", min_value=0, max_value=5, value=3)
    baggage_handling = st.slider("Baggage handling", min_value=0, max_value=5, value=3)
    checkin_service = st.slider("Checkin service", min_value=0, max_value=5, value=3)
    cleanliness = st.slider("Cleanliness", min_value=0, max_value=5, value=3)
    online_boarding = st.slider("Online boarding", min_value=0, max_value=5, value=3)
    departure_delay = st.number_input("Departure Delay in Minutes", min_value=0, max_value=10000, value=0)
    arrival_delay = st.number_input("Arrival Delay in Minutes", min_value=0, max_value=10000, value=0)

    # Create a DataFrame with the input data
    input_data = pd.DataFrame({
        'Customer Type': [customer_type],
        'Class': [travel_class],
        'Type of Travel': [travel_type],
        'Age': [age],
        'Flight Distance': [flight_distance],
        'Seat comfort': [seat_comfort],
        'Food and drink': [food_drink],
        'Inflight wifi service': [inflight_wifi_service],
        'Inflight entertainment': [inflight_entertainment],
        'Online support': [online_support],
        'Ease of Online booking': [online_booking],
        'On-board service': [onboard_service],
        'Leg room service': [leg_room_service],
        'Baggage handling': [baggage_handling],
        'Checkin service': [checkin_service],
        'Cleanliness': [cleanliness],
        'Online boarding': [online_boarding],
        'Departure Delay in Minutes': [departure_delay],
        'Arrival Delay in Minutes': [arrival_delay]
    })

    # Initialize session state variables
    if 'prediction' not in st.session_state:
        st.session_state.prediction = None
    if 'show_recommendations' not in st.session_state:
        st.session_state.show_recommendations = False

    # Predict the customer satisfaction
    if st.button("Predict"):
        # Apply the same preprocessing as during training
        input_features = model.named_steps['preprocessor'].transform(input_data)
        prediction = model.named_steps['classifier'].predict(input_features)[0]
        st.session_state.prediction = 'Satisfied' if prediction == 0 else 'Dissatisfied'
        st.session_state.show_recommendations = False

    # Display the prediction result and recommendations (including color coding)
    if st.session_state.prediction:
        color = "lightgreen" if st.session_state.prediction == 'Satisfied' else "lightcoral"
        st.markdown(
            f"<div style='background-color: {color}; padding: 10px; border-radius: 5px;'>"
            f"<b>Predicted Satisfaction:</b> {st.session_state.prediction}"
            "</div>",
            unsafe_allow_html=True
        )
        # Show recommendations for dissatisfied customers
        if st.session_state.prediction == 'Dissatisfied':
            # Insert empty line
            st.write("")
            if st.button("Show Recommendations"):
                st.session_state.show_recommendations = True

            if st.session_state.show_recommendations:
                st.write("Based on the customer profile, here are some recommendations to improve satisfaction:")
                recommendations = {
                    '**Seat comfort**': "Consider upgrading the seating comfort to improve customer satisfaction.",
                    '**Food and drink**': "Enhance the quality and variety of food and drinks offered during the flight.",
                    '**Inflight wifi service**': "Improve the reliability and speed of inflight WiFi services.",
                    '**Inflight entertainment**': "Provide a wider selection of entertainment options including movies, music, and games.",
                    '**Online support**': "Enhance online support with quicker response times and more helpful information.",
                    '**Ease of Online booking**': "Simplify the online booking process and ensure the website is user-friendly.",
                    '**On-board service**': "Train staff to be more attentive and responsive to customer needs during the flight.",
                    '**Leg room service**': "Increase the legroom available to passengers to make their flight more comfortable.",
                    '**Baggage handling**': "Ensure that baggage handling is efficient and that luggage is delivered promptly.",
                    '**Checkin service**': "Streamline the check-in process and reduce waiting times.",
                    '**Cleanliness**': "Maintain high standards of cleanliness throughout the flight.",
                    '**Online boarding**': "Improve the online boarding process for a smoother experience."
                }

                for feature, recommendation in recommendations.items():
                    st.write(f"- {recommendation}")

if __name__ == "__main__":
    show_page()