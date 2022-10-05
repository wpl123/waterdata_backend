
# Waterdata Backend

This repository contains all the code required to create and interegate a MySQL Water database for the Maules Creek catchment

# Brief explanation of the supdirectories;

- app - Python Code to extract, transform and load groundwater, surfacewater and rainfall data from public sources and store in a MySQL database
- app-api - FastAPI to enable access to MySQL db
- dockerfiles - dockerfiles for system build
- frontend - Jupytr Notebooks to plot water data and implement machine learning (LSTM) to investigate anomalies of groundwater data
- frontend/app-dash - dashboard in Plotly Dash
- data - log directories 

# Use the adminer tool to add data to the following tables
- meters
- meter_types
- errors

# To update the database

- One off; run the script run_load_waterdata.sh 
- Daily; cron --> $WATER_DIR/waterdata_backend/run_load_waterdata.sh >> $WATER_DIR/waterdata_backend/data/downloads/cronlog/cron.log 2>&

Links to data;

- nsw - https://realtimedata.waternsw.com.au/
- vic - https://data.water.vic.gov.au/
- qld - https://water-monitoring.information.qld.gov.au/


Link to Kysters API Reference - https://water-monitoring.information.qld.gov.au/wini/Documents/RDMW_API_doco.pdf


# Brief Explanation of meter and meter_types tables