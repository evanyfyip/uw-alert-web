from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px

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
    # sample alerts
    alert_coords = [[47.663082, -122.310859], [47.658377, -122.317777]]
    alert_messages = ["Police looking for man with handgun on 47th St. near 16th Ave. Secure doors, avoid area if possible.",
                      "Shooting reported near 42nd Ave NE/Roosevelt at 12:46pm. Shooter fled in white vehicle."]
    map = get_folium_map(alert_coords, alert_messages)
    return render_template('/base.html', map_html=map)

if __name__ == '__main__':
    app.run(debug=True)
