# -*- coding: utf-8 -*-
"""appy.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OHn6jquYj2MdqkXGbpu4szF3JA-mDoUf
"""

import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# Load the datasets
merged_df = pd.read_csv('/content/merged_data.csv')
price_df = pd.read_csv('/content/price_data.csv')
weather_df = pd.read_csv('/content/weather_data.csv')

# Load trained models
price_model = load_model('/content/models/price_model.h5')
weather_model = load_model('/content/models/weather_model.h5')

def main():
    st.title("Maize Price and Weather Prediction in Kenya")
    st.markdown("""
    <style>
    .main {
        background-color: #F5F5F5;
    }
    </style>
    """, unsafe_allow_html=True)

    # Load the regions and counties
    regions = merged_df['Regions'].unique()
    counties = merged_df['County'].unique()

    # Select region and county
    selected_region = st.selectbox("Select Region", regions)
    selected_county = st.selectbox("Select County", counties)

    # Input fields
    year = st.number_input('Year', min_value=2023, max_value=2100, step=1)
    month = st.number_input('Month', min_value=1, max_value=12, step=1)

    # Predict button
    if st.button('Predict'):
        # Filter the data for the selected county and region
        county_region_data = merged_df[(merged_df['County'] == selected_county) & (merged_df['Regions'] == selected_region)]

        # Calculate mean values for the required features
        mean_amount_produced = county_region_data['Amount Produced'].mean()
        mean_annual_rainfall = county_region_data['Annual Rainfall'].mean()
        mean_annual_temperature = county_region_data['Annual Temperature'].mean()

        # Prepare the input data for prediction
        input_data = np.array([[year, month, mean_amount_produced, mean_annual_rainfall, mean_annual_temperature]])

        # Predict maize price
        price_prediction = price_model.predict(input_data)
        st.write(f'Predicted Maize Price for {selected_county} in {selected_region}: {price_prediction[0][0]}')

        # Predict weather
        weather_prediction = weather_model.predict(input_data[:, :2])
        st.write(f'Predicted Annual Rainfall for {selected_county} in {selected_region}: {weather_prediction[0][0]}')
        st.write(f'Predicted Annual Temperature for {selected_county} in {selected_region}: {weather_prediction[0][1]}')

if __name__ == '__main__':
    main()