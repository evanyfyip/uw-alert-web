# uw-alert-web
## Group Members:
- James Joko
- John Michael
- Mark Qiao
- Evan Yip

## Project Type: Tool

## Questions of Interest
- What area around UW campus is most commonly listed in alerts?
- What time of day do alerts occur more often?
- What is the most common type of incident?
- Have any trends arisen across time in the UW alert system?

## Goals for the Project
- Create a web application and visualization of the UW campus and surrounding area.
- Parse real-time information from the UW alerts system and display the alert's origin.
- Inform the user of alert trends over time and location

## Data Sources
- Seattle GeoData
  - GIS database for Seattle streets that allows for map visualizations
  - Link: https://data-seattlecitygis.opendata.arcgis.com/datasets/SeattleCityGIS::seattle-streets-3/explore?location=47.609360%2C-122.325916%2C14.88
- UW Alerts Blog
  - Official blogpost maintained by the University of Washington dedicated to reporting incidents may affect students
  - Link: https://emergency.uw.edu/?_gl=1*ztz313*_ga*MzIwNzY5MTg2LjE2NjU4NzU5NjU.*_ga_3T65WK0BM8*MTY3NjMyNTM5Ny4yMS4wLjE2NzYzMjU0MDEuMC4wLjA.

Instructions:
- Pull on main to get the latest version of the application
- conda env create -f environment.yml
- conda activate uw_alerts_env
- python app.py 
