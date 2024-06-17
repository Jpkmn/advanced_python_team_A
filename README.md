# Final Project in Advanced Programming with Python - Airline Customer Satisfaction Prediction

## Group A
Moritz Hütteneder, Ting Jin, Nobin Kachirayil, Joel Pascal Kömen, Ankit Pani, Claudio Maximilian Thumm, Yuchen Wang

## Introduction
The dataset at hand offers a comprehensive overview of customer satisfaction levels (satisfied or dissatisfied) within an undisclosed airline company. The dataset is extensive, initially encompassing 22 columns and 129,880 rows of detailed information. This rich dataset serves as a foundation to predict future customer satisfaction based on various influential parameters.

These parameters encompass a broad spectrum of factors affecting customer satisfaction, including flight punctuality, service quality, and more. By analyzing this dataset, airlines can glean critical insights into the determinants of customer satisfaction, enabling them to tailor their services to significantly enhance the overall customer experience.

## Project Goal
This project follows two goals: 
1. Train several machine learning models on this dataset and identify the most effective model for predicting customer satisfaction. 
2. Build a dashboard, based on the best model, that allows airlines to predict customer satisfaction based on the input of various parameters.

## What is the utility of the dashboard?
The prototype provides a comprehensive and interactive analysis of airline customer satisfaction data. 
By leveraging a machine learning model, airlines can predict individual and batch customer satisfaction which offers actionable insights to improve service quality of an airline
and identify the most important factors to enhance customer satisfaction. 
Batch data, e.g., from a survey, can be uploaded to the application, and the model will predict the satisfaction of each customer.
The detailed analysis section, with its visualizations and filters, allows stakeholders to explore key metrics and trends, identify areas of improvement, and make data-driven 
decisions to enhance overall customer experience. This makes the application valuable for airline management, customer service teams, and data analysts aiming to optimize customer satisfaction 
and operational efficiency.

## Structure of the repository
The repository is structured as follows:
- Folder `Final Project`: Contains the main files and folders of the project. Inside this folder, the following structure can be found: 
  - Folder `data`: Contains the dataset initially downloaded from Kaggle (airline_customer_satisfaction_original.csv) and the dataset used for training the model (Airline_customer_satisfaction.csv).
  - `Model Airline Satisfaction.ipynb`: The Jupyter notebook containing the data exploration, the training of six different model, and evaluation process.
  - `Final Presentation.pdf`: The final presentation of the project.
  - Folder `Dashboard`: Contains the main files and folders of the dashboard application.
    - Folder `data`: Contains the cleaned dataset for the dashboard (airline_customer_satisfaction.csv).
    - `pages`: Contains the model (XGBoost) and main pages of the application, including the home page, the detailed analysis page, the prediction pages, and feature importance page.
    - `app.py`: The main file to run the application.
    - `sample_airline_customer_satisfaction.xlsx`: Prepared dataset for uploading batch data to the application.

## Explanation of the files and dashboard execution
- Please explore the file `Model Airline Satisfaction.ipynb` to understand the data exploration, the training of six different models, and the evaluation process.
- To run the dashboard, navigate to the folder `Dashboard` (in your terminal: `cd Final Project/Dashboard`) and execute the file `app.py` in your console with the command `streamlit run app.py`. Please make sure that all necessary libraries are installed before running the dashboard.