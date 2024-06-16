# batch_prediction.py
import streamlit as st
import pandas as pd
import joblib
import io

# Method to show the batch prediction page
def show_page():
    st.title("Batch Prediction for Customer Satisfaction")
    st.write("Upload an Excel file with customer data, e.g., based on a survey sent out after flights, "
             "to predict customer satisfaction.")
    st.write("""
    The following features are required for the prediction:
    - **Customer Type**: 'Loyal Customer' or 'disloyal Customer'
    - **Class**: 'Eco', 'Eco Plus', or 'Business'
    - **Type of Travel**: 'Business travel' or 'Personal Travel'
    - **Age**: Customer's age, e.g., 25
    - **Flight Distance**: Distance of the flight in miles, e.g., 500
    - **Seat comfort**: Rating from 0 to 5
    - **Food and drink**: Rating from 0 to 5
    - **Inflight wifi service**: Rating from 0 to 5
    - **Inflight entertainment**: Rating from 0 to 5
    - **Online support**: Rating from 0 to 5
    - **Ease of Online booking**: Rating from 0 to 5
    - **On-board service**: Rating from 0 to 5
    - **Leg room service**: Rating from 0 to 5
    - **Baggage handling**: Rating from 0 to 5
    - **Checkin service**: Rating from 0 to 5
    - **Cleanliness**: Rating from 0 to 5
    - **Online boarding**: Rating from 0 to 5
    - **Departure Delay in Minutes**: Delay in minutes, e.g., 10
    - **Arrival Delay in Minutes**: Delay in minutes, e.g., 5
    """)

    st.subheader("Please adhere to the structure of the following template:")
    # Create template data for download
    template_data = pd.DataFrame({
        'Customer Type': ['Loyal Customer', 'disloyal Customer', 'Loyal Customer', 'disloyal Customer', 'disloyal Customer'],
        'Class': ['Eco', 'Eco Plus', 'Business', 'Eco', 'Business'],
        'Type of Travel': ['Business travel', 'Personal Travel', 'Business travel', 'Personal Travel', 'Personal Travel'],
        'Age': [35, 45, 60, 25, 40],
        'Flight Distance': [500, 1500, 200, 1000, 3000],
        'Seat comfort': [3, 4, 5, 2, 3],
        'Food and drink': [4, 5, 1, 3, 2],
        'Inflight wifi service': [2, 3, 5, 1, 4],
        'Inflight entertainment': [4, 5, 2, 3, 1],
        'Online support': [3, 4, 4, 2, 3],
        'Ease of Online booking': [4, 5, 4, 3, 2],
        'On-board service': [4, 5, 2, 3, 1],
        'Leg room service': [3, 4, 5, 2, 3],
        'Baggage handling': [4, 5, 1, 3, 2],
        'Checkin service': [4, 5, 3, 1, 2],
        'Cleanliness': [5, 4, 5, 3, 2],
        'Online boarding': [4, 5, 1, 3, 2],
        'Departure Delay in Minutes': [10, 20, 100, 5, 30],
        'Arrival Delay in Minutes': [15, 25, 200, 10, 40]
    })

    # Save the template to a BytesIO object
    template_file = io.BytesIO()
    template_data.to_excel(template_file, index=False)
    template_file.seek(0)

    # Provide download button for the template
    st.download_button(label='Download Template',
                       data=template_file,
                       file_name='template_airline_customer_satisfaction.xlsx',
                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    st.subheader("Upload Excel File for Prediction")

    # File uploader for Excel file
    uploaded_file = st.file_uploader("Upload an Excel file with customer data", type=["xlsx"])

    if uploaded_file:
        # Read the Excel file
        input_df = pd.read_excel(uploaded_file)

        # Display the input data
        st.write("Input Data", input_df)

        # Predict customer satisfaction with the uploaded data
        if st.button("Predict Batch Satisfaction"):
            model = joblib.load('./pages/xgboost.pkl')
            predictions = model.predict(input_df)
            input_df['Predicted Satisfaction'] = ['Dissatisfied' if pred == 1 else 'Satisfied' for pred in predictions]

            # Display results of the batch prediction
            st.write("Prediction Results (see last column of dataframe)", input_df)

            # Calculate the number of satisfied customers
            num_satisfied = (input_df['Predicted Satisfaction'] == 'Satisfied').sum()
            total_customers = input_df.shape[0]
            st.write(f"Number of Satisfied Customers: {num_satisfied} out of {total_customers}")
            st.write(f"Percentage of Satisfied Customers: {num_satisfied / total_customers * 100:.2f}%")

if __name__ == "__main__":
    show_page()