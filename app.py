from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import folium
import sys
import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

# Our modules
from visualization_manager.visualization_manager import get_folium_map


app = Flask(__name__)

@app.route('/')
def plot_folium_map():
    map = get_folium_map()
    return render_template('/base.html', map_html=map)

@app.route('/update_map',methods=['POST'])
def update_map():
    new_data = request.form['text-input']
    #TODO: combine all modules here to update the map
    return new_data

@app.route('/change_map')
def change_map():
    map = folium.Map(location=[51.5074, -0.1278], zoom_start=10)
    map_html = map.get_root().render()
    return map_html

if __name__ == '__main__':
    app.run(debug=True)
