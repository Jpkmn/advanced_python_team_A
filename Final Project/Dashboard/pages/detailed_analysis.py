# detailed_analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Method to show the detailed analysis page
def show_page():
    st.title("Detailed Analysis")

    st.write("This page provides detailed analysis of the airline customer satisfaction data which was used to train the model. "
             "Several visualizations are included to help understand the distribution of customer satisfaction, customer types, classes, and "
             "other key features. Use the filters in the sidebar to explore specific segments of the data.")

    # Sidebar filters
    st.sidebar.header("Filters")
    df = pd.read_csv('./data/Airline_customer_satisfaction.csv')
    customer_type = st.sidebar.multiselect("Customer Type", options=df["Customer Type"].unique(),
                                           default=df["Customer Type"].unique())
    travel_type = st.sidebar.multiselect("Type of Travel", options=df["Type of Travel"].unique(),
                                         default=df["Type of Travel"].unique())
    travel_class = st.sidebar.multiselect("Class", options=df["Class"].unique(), default=df["Class"].unique())

    # Add age slider
    min_age = int(df['Age'].min())
    max_age = int(df['Age'].max())
    age_range = st.sidebar.slider("Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

    # Filter data based on selections
    filtered_df = df[(df["Customer Type"].isin(customer_type)) &
                     (df["Type of Travel"].isin(travel_type)) &
                     (df["Class"].isin(travel_class)) &
                     (df["Age"] >= age_range[0]) &
                     (df["Age"] <= age_range[1])].copy()

    # Calculate metrics
    avg_departure_delay = filtered_df['Departure Delay in Minutes'].mean()
    avg_arrival_delay = filtered_df['Arrival Delay in Minutes'].mean()
    avg_flight_distance = filtered_df['Flight Distance'].mean()
    avg_customer_age = filtered_df['Age'].mean()
    percent_satisfied = (filtered_df['satisfaction'] == 'satisfied').mean() * 100

    # Calculate the most booked class and its percentage
    most_booked_class = filtered_df['Class'].value_counts().idxmax()

    # Display metrics
    st.subheader("Key Metrics")
    st.write("The following metrics provide an overview of the data's most important KPIs based on the selected filters.")
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col1.metric("Avg Departure Delay (min)", f"{avg_departure_delay:.2f}")
    col2.metric("Avg Arrival Delay (min)", f"{avg_arrival_delay:.2f}")
    col3.metric("Avg Flight Distance (miles)", f"{avg_flight_distance:.2f}")
    col4.metric("Avg Customer Age", f"{avg_customer_age:.2f}")
    col5.metric("% Satisfied Customers", f"{percent_satisfied:.2f}%")
    col6.metric("Most Booked Class", f"{most_booked_class}")

    st.header("Satisfaction Distribution")
    st.write("The following chart shows the distribution of customer satisfaction.")
    fig = px.pie(filtered_df, names='satisfaction', title='Satisfaction Distribution')
    st.plotly_chart(fig)

    # Count the number of customers per customer type
    customer_type_count = filtered_df['Customer Type'].value_counts().reset_index()
    customer_type_count.columns = ['Customer Type', 'Number of Customers']

    # Calculate the percentage
    total_customers = customer_type_count['Number of Customers'].sum()
    customer_type_count['Percentage'] = 100 * customer_type_count['Number of Customers'] / total_customers

    # Format the percentage to two decimal points
    customer_type_count['Percentage'] = customer_type_count['Percentage'].apply(lambda x: f"{x:.2f}%")

    # Create the bar chart
    st.header("Customer Type Distribution")
    st.write("The following chart shows the distribution of customer types.")
    fig = px.bar(customer_type_count, x='Customer Type', y='Number of Customers',
                 title='Customer Type Distribution',
                 hover_data={'Customer Type': True,
                             'Number of Customers': True,
                             'Percentage': True})
    st.plotly_chart(fig)

    # Count the number of customers per class
    class_count = filtered_df['Class'].value_counts().reset_index()
    class_count.columns = ['Class', 'Number of Customers']

    # Calculate the percentage
    total_customers = class_count['Number of Customers'].sum()
    class_count['Percentage'] = 100 * class_count['Number of Customers'] / total_customers

    # Format the percentage to two decimal points
    class_count['Percentage'] = class_count['Percentage'].apply(lambda x: f"{x:.2f}%")

    # Create the bar chart
    st.header("Class Distribution")
    st.write("The following chart shows the distribution of classes booked by the customers.")
    fig = px.bar(class_count, x='Class', y='Number of Customers',
                 title='Class Distribution',
                 hover_data={'Class': True,
                             'Number of Customers': True,
                             'Percentage': True})  # Ensure Percentage is shown
    st.plotly_chart(fig)

    st.header("Age Distribution")
    st.write("The following chart shows the distribution of customer ages.")
    fig = px.histogram(filtered_df, x='Age', title='Age Distribution', nbins=30)
    fig.update_traces(marker_line_color='white', marker_line_width=1.5)
    st.plotly_chart(fig)

    # Group ages into bins
    age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
    age_labels = ['<18', '18-25', '25-35', '35-45', '45-55', '55-65', '65+']
    filtered_df['Age Group'] = pd.cut(filtered_df['Age'], bins=age_bins, labels=age_labels, right=False)
    # Calculate satisfaction by age group
    satisfaction_by_age_group = filtered_df.groupby('Age Group', observed=False)['satisfaction'].value_counts(
        normalize=True).unstack().fillna(0) * 100

    st.header("Satisfaction by Age Group")
    st.write(
        "The following chart shows the percentage of satisfied and dissatisfied customers in each age group and helps "
        "understand which age group is dissatisfied the most.")
    fig = px.bar(satisfaction_by_age_group, barmode='group', title='Satisfaction by Age Group',
                 labels={'value': 'Percentage'},
                 hover_data={'value': ':.2f'})  # Format hover data to two decimal places

    # Ensure the percentage sign is displayed correctly in hover data and include age group
    fig.update_traces(
        hovertemplate='Age Group: %{x}<br>Satisfaction: %{y:.2f}%<extra></extra>'
    )

    st.plotly_chart(fig)

    # Show additional visualizations (box plots) for further analysis of the data
    st.header("Satisfaction vs Services")
    st.write("The following box plots show the distribution of service ratings for satisfied and dissatisfied customers. "
             "It helps identify which services have the most impact on customer satisfaction.")
    service_features = ['Seat comfort', 'Food and drink', 'Inflight wifi service', 'Inflight entertainment',
                        'Online support', 'Ease of Online booking', 'On-board service', 'Leg room service',
                        'Baggage handling', 'Checkin service', 'Cleanliness', 'Online boarding']

    for feature in service_features:
        fig = px.box(filtered_df, x='satisfaction', y=feature, title=f'{feature} vs Satisfaction')
        st.plotly_chart(fig)

    # Scatter plot for flight distance vs satisfaction
    st.header("Flight Distance vs Satisfaction")
    st.write("The following scatter plot shows the relationship between flight distance and customer satisfaction. "
             "It helps understand if longer flights lead to more dissatisfaction.")
    fig = px.scatter(filtered_df, x='Flight Distance', y='satisfaction', title='Flight Distance vs Satisfaction',
                     color='satisfaction')
    st.plotly_chart(fig)

    # Scatter plot for departure delay vs arrival delay
    st.header("Departure Delay vs Arrival Delay")
    st.write("The following scatter plot shows the relationship between departure delay and arrival delay. "
             "It helps understand if delays in departure lead to delays in arrival and if they impact customer satisfaction.")
    fig = px.scatter(filtered_df, x='Departure Delay in Minutes', y='Arrival Delay in Minutes',
                     title='Departure Delay vs Arrival Delay', color='satisfaction')
    st.plotly_chart(fig)

if __name__ == "__main__":
    show_page()