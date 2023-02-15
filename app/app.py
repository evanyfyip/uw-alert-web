from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px

import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go


app = Flask(__name__)


@app.route('/')
def bar_with_plotly():
    gdf = gpd.read_file('./data/SeattleGISData/Seattle_Streets.geojson')
    lat_list = []
    lon_list = []
    lon1 = []
    lon2 = []
    lat1 = []
    lat2 = []
    for street in gdf['geometry']:
        coords = np.array(street.coords)
        lon1.append(coords[0, 0])
        lon2.append(coords[1, 0])
        lat1.append(coords[0, 1])
        lat2.append(coords[1, 1])
    gdf['lon1'] = lon1
    gdf['lon2'] = lon2
    gdf['lat1'] = lat1
    gdf['lat2'] = lat2

    longitude_bounds = (-122.2980, -122.3230)
    latitude_bounds = (47.67657, 47.6499)
    # Filtering for udistrict
    lon1_filt = (gdf['lon1'] > longitude_bounds[1]) & (
        gdf['lon1'] <= longitude_bounds[0])
    lon2_filt = (gdf['lon2'] > longitude_bounds[1]) & (
        gdf['lon2'] <= longitude_bounds[0])

    lat1_filt = (gdf['lat1'] > latitude_bounds[1]) & (
        gdf['lat1'] <= latitude_bounds[0])
    lat2_filt = (gdf['lat2'] > latitude_bounds[1]) & (
        gdf['lat2'] <= latitude_bounds[0])

    udist_gdf = gdf[lon1_filt & lat1_filt & lon2_filt & lat2_filt]

    lat_list = []
    lon_list = []
    for street in udist_gdf['geometry']:
        coords = np.array(street.coords)
        lon_list.append(coords[0, 0])
        lon_list.append(coords[1, 0])
        lon_list.append(None)
        lat_list.append(coords[0, 1])
        lat_list.append(coords[1, 1])
        lat_list.append(None)
    fig = go.Figure(
        data=[
            go.Scattermapbox(
                lat=lat_list,
                lon=lon_list,
                text=udist_gdf['UNITDESC'],
                mode='lines',
                marker=go.scattermapbox.Marker(size=14)
            )
        ]
    )

    access_token = 'pk.eyJ1IjoiZXZhbnlpcCIsImEiOiJjbGRxYnc3dXEwNWxxM25vNjRocHlsOHFyIn0.0H4RiKd8X94CeoXwEd4TgQ'
    # zoom=12.5, color_discrete_sequence=['#EA4630']
    fig.update_layout(
        mapbox={
            'style': "dark",
            'accesstoken': access_token,
            'center': go.layout.mapbox.Center(
                lat=47.6648928,
                lon=-122.3119374
            ),
            'zoom': 13,
        },
        height=900,
        width=1000,

    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('base.html', graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(debug=True)
