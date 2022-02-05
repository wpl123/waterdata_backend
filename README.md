
Waterdata Backend

This repository contains all the code required to create and interegate a MySQL Water database for the Maules Creek catchment

Brief explanation of the supdirectories;

app - Python Code to extract, transform and load groundwater, surfacewater and rainfall data from public sources and store in a MySQL database
app-api - Flask Api to enable access to MySQL db
dockerfiles - dockerfiles for system build
frontend - Jupytr Notebooks to plot water data and implement machine learning (LSTM) to investigate anomalies of groundwater data
frontend/app-dash - dashboard in Plotly Dash

