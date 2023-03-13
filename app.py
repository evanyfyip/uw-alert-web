"""
Initializes a web application for UW Alerts Visualization
"""

import os
import ast
import io
import folium
import pandas as pd
import openai
import googlemaps

from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

# Our modules
from visualization_manager.visualization_manager import get_folium_map
from visualization_manager.visualization_manager import get_urgent_incidents
from parse_uw_alerts import parse_uw_alerts

app = Flask(__name__)

@app.route('/')
def plot_folium_map():
    """
    Render the leaflet map upon app startup
    """
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "data/uw_alerts_clean.csv")
    alert_df = pd.read_csv(filename)
    map_html = get_folium_map(get_urgent_incidents(alert_df, time_frame=10))
    return render_template('/base.html', map_html=map_html)

@app.route('/submit', methods=['POST'])
def submit():
    """
    Change the map when a user inputs an alert.
    """
    return redirect(url_for('plot_folium_map'))

@app.route('/demo', methods=['GET'])
def demo():
    """
    Render the "demo" page for in-class presentations.
    """
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "data/uw_alerts_clean.csv")
    alert_df = pd.read_csv(filename, converters = {'geometry': ast.literal_eval})
    map_html = get_folium_map(get_urgent_incidents(alert_df, time_frame=10))
    return render_template('/demo.html', map_html=map_html)

@app.route('/update_map',methods=['POST'])
def update_map():
    """
    Update the map when a new alert is posted.
    """
    load_dotenv('./env')
    openai.api_key = os.getenv('OPENAI_API_KEY')
    print(openai.api_key)
    uw_alert_filepath='./data/uw_alerts_clean.csv'
    uw_alerts = pd.read_csv(uw_alert_filepath,index_col=False)
    new_data = request.form['text-input']
    buf = io.StringIO(new_data)
    gpt_output = parse_uw_alerts.prompt_gpt(buf.readlines(),return_alert_type=True)
    google_maps_api_key=os.getenv('GOOGLE_MAPS_API_KEY')
    gmaps = googlemaps.Client(key=google_maps_api_key)
    cleaned_gpt_output = parse_uw_alerts.generate_ids(uw_alert_filepath,gpt_table=gpt_output[0],
                                                      alert_type=gpt_output[1])
    gpt_table = parse_uw_alerts.clean_gpt_output(gpt_output = cleaned_gpt_output,gmaps_client=gmaps)
    uw_alerts =pd.concat([gpt_table,uw_alerts],ignore_index=True)
    uw_alerts.to_csv(uw_alert_filepath,index=False)
    #send cleaned csv into viz manager
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "data/uw_alerts_clean.csv")
    alert_df = pd.read_csv(filename, converters = {'geometry': ast.literal_eval})
    map_html = get_folium_map(get_urgent_incidents(alert_df, time_frame=2))
    return render_template('/demo.html', map_html=map_html)

@app.route('/change_map')
def change_map():
    """
    Change the map when a user inputs an alert.
    """
    return folium.Map(location=[51.5074, -0.1278], zoom_start=10).get_root().render()

if __name__ == '__main__':
    app.run(debug=True)
