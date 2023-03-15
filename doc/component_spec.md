# Component Specification 

## Software Component

**1. Server:**
- Modules: `uw-alerts-web.py`
- Static: `main.css`, `about.css`
- Templates: `home.html`, `demo.html`, `about.html`, `past.html`

The server implements the front end and back end connection by using flask to display a plotly plot through HTML and javascript on a webpage. 
The inputs to this component are an html map and metadata produced by the Visualization Manager. The server returns a render template that is passed through to the html pages listed in the templates above. The server also handles user navigation, styling, and requests to update the map with new information.

**2. Visualization Manager:**
- Module: `visualization_manager.py`

Description:
The visualization manager implements the creation of a folium plot using data scraped from the UW Alerts Webpage and returns a rendered interactive html map that is passed to the front end manager. This plot consists of an interactive leaflet map with markers and popups to indicate the locations of current incidents around U-district. The visualization manager requires numerous python packages, ranging from pandas, geopandas, folium, and matplotlib. It also requires a csv file which indicates incidents of crime and the area. This csv is produced by the Text Manager which scrapes the UW alerts website.

**3. Web Parser:**
- Module: `parse_uw_alerts.py`

Description:
The web parser implements the parsing/scraping of the UW alerts website in order to update the application with new incidents of crime. The primary module is parse_uw_alerts which utilizes multiple different functions to scrape the website. The process is as follows:

1. `scrape_uw_alerts()`: scrapes the uw alerts blog for alert descriptions
2. `prompt_gpt()`: Sends the text from the blog to ChatGPT to convert from free text format to a structured format
3. `generate_ids()`: Generates unique Alert IDs and Incident IDs for each alert
4. `clean_gpt_output()`: Cleans the table and passes the address to Google maps API to get a latitude and longitude which will call `prompt_gpt()` then `generate_ids()` then `clean_gpt_output()` will save the final output to uw_alerts_clean.csv

The web parser requires the following dependencies: os, io, time, re, pandas, openai, transformers, googlemaps, dotenv, bs4 and requests

The web parser returns the csv file with incidents with the following columns:
- Alert ID
- Incident ID
- Date
- Report Time
- Incident Time
- Nearest Address to Incident
- Incident Category
- Incident Summary
- Incident Alert
- Alert Type
- Google Address
- geometry

## Preliminary Plan
1. Develop map interface locally
2. Clean UW Alerts text data to obtain key incident information.
3. Develop method to update live map when a new incident is reported on UW Alerts. 

## Interaction Diagram
![UW Alerts Map_ Component Interaction Diagram](https://user-images.githubusercontent.com/50302514/225177570-a27da450-6494-4d5d-87a5-f0e3bee54391.png)


