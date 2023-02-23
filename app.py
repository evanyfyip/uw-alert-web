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
    map = get_folium_map()
    return render_template('/base.html', map_html=map)

if __name__ == '__main__':
    app.run(debug=True)
