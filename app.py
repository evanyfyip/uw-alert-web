from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
import plotly
import os
import plotly.express as px
import folium
import sys
import ast
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go


# Our modules
from visualization_manager.visualization_manager import get_folium_map
<<<<<<< Updated upstream
from visualization_manager.visualization_manager import get_urgent_incidents

=======
import parse_uw_alerts
>>>>>>> Stashed changes

app = Flask(__name__)

@app.route('/')
def plot_folium_map():
    # sample alerts
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "data/uw_alerts_clean.csv")
    alert_df = pd.read_csv(filename, converters = {'geometry': ast.literal_eval})
    map, marker_dict = get_folium_map(get_urgent_incidents(alert_df, 4))
    # print(marker_dict)
    return render_template('/base.html', map_html=map)


@app.route('/update_map',methods=['POST'])
def update_map():
    load_dotenv('./env')
    uw_alert_filepath='./data/uw_alerts_clean.csv'
    uw_alerts = pd.read_csv(uw_alert_filepath,index_col=False)
    last_alert=uw_alerts['Incident Alert'].values[0]
    new_data = request.form['text-input']
    buf = io.stringIO(new_data)
    gpt_output = parse_uw_alerts.prompt_gpt(buf.readlines(),return_alert_type=True)
    GOOGLE_MAPS_API_KEY=os.getenv('GOOGLE_MAPS_API_KEY')
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    cleaned_gpt_output = parse_uw_alerts.generate_ids(uw_alert_filepath,gpt_table=gpt_output[0],alert_type=gpt_output[1])
    gpt_table = parse_uw_alerts.clean_gpt_output(gpt_output = cleaned_gpt_output,gmaps_client=gmaps)
    uw_alerts =pd.concat([gpt_table,uw_alerts],ignore_index=True)
    uw_alerts.to_csv(uw_alert_filepath,index=False)

    #TODO: combine all modules here to update the map
    return new_data

@app.route('/change_map')
def change_map():
    map = folium.Map(location=[51.5074, -0.1278], zoom_start=10)
    map_html = map.get_root().render()
    return map_html

if __name__ == '__main__':
    app.run(debug=True)
