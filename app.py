from flask import Flask, render_template
import json
import plotly
import os
import plotly.express as px

import sys
import ast
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
    # sample alerts
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "data/uw_alerts_clean.csv")
    alert_df = pd.read_csv(filename, converters = {'geometry': ast.literal_eval}).head(5)
    map, marker_dict = get_folium_map(alert_df)
    # print(marker_dict)
    return render_template('/base.html', map_html=map)

if __name__ == '__main__':
    app.run(debug=True)
