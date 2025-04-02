# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 15:07:55 2025

@author: Anna
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# load dataset
#file_path = r"C:\Users\Anna\Documents\JOB SEARCHING\Portfolio & Tests\Air quality NY\Air_Quality_NY.csv"
file_path = "Air_Quality_NY.csv"
df = pd.read_csv(file_path)

# preparation


df['Year'] = df['Time Period'].str.extract(r'(\d{4})')  
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna(subset=['Year'])  
df['Year'] = df['Year'].astype(int)



# slider
st.title("NYC Air Quality Dashboard")
# filter data by condition
filtered_df_slider = df[df["Data Value"] > 10]

# displaying a table with filtered data
st.write("## Data with pollution > 10")
st.dataframe(filtered_df_slider)

# create a dynamic slider
threshold = st.slider("Select the pollution threshold", min_value=0, max_value=100, value=10)

# filter data
filtered_df_slider_dynamic = df[df["Data Value"] > threshold]

# display filtered data by threshold
st.write(f"## Data with pollution > {threshold}")
st.dataframe(filtered_df_slider_dynamic)





# streamlit UI
st.write("Explore air pollution trends across different neighborhoods.")

# dropdown for neighborhood selection
neighborhoods = df["Geo Place Name"].unique()
selected_neighborhood = st.selectbox("Select a Neighborhood:", neighborhoods)

# filter data based on selected neighborhood
filtered_df = df[df["Geo Place Name"] == selected_neighborhood]

filtered_df = filtered_df.sort_values(by='Year')
filtered_df = filtered_df.groupby(['Year', 'Name'])['Data Value'].mean().reset_index()

# create scatter plot
fig = px.scatter(
    filtered_df, 
    x="Year", 
    y="Data Value", 
    color="Name", #type of pollutant
    title=f"Air Quality Trends in {selected_neighborhood}",
    labels={"Year": "Year", "Data Value": "Pollution Level", "Name": "Pollutant"},
    hover_data=["Name"]
)

# display the plot
st.plotly_chart(fig)

# show filtered data
st.write("Filtered Data:")
st.dataframe(filtered_df)
