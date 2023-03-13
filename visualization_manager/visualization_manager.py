"""
Name: Visualization Manager
What it does:
- Renders an interactive street map visualization
    - highlights specific streets of interest
- Includes details of uw alert events
inputs:
- street:
- alert_type:
- description:
- time:

outputs:
- interactive street visualization
"""

from datetime import datetime, timedelta
import os
import pyproj
import folium
from folium.plugins import HeatMap
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import nearest_points, transform

def get_urgent_incidents(alerts_df, time_frame):
    """
    Retrieves and filters the uw_alerts_clean.csv
    for the incidents that occured today.

    Parameters
    ----------
    time_frame

    Returns
    -------
    urgent_incidents_df : Dataframe
        Pandas dataframe of the most urgent incidents
    """
    # Checking columns
    cols = ['Incident ID', 'Alert ID', 'Date', 'Report Time']
    for col in cols:
        if col not in alerts_df.columns.to_list():
            raise ValueError("Invalid alerts_df schema")

    # Step 1: Extract dataframe of alerts with Report time
    report_times_df = alerts_df[~alerts_df['Report Time'].isna()].copy()
    # Filter by time. Remove alerts beyond time cutoff
    report_times_df.loc[:, 'report_datetime'] = pd.to_datetime(
        report_times_df['Date'] + \
        ' ' + \
        report_times_df['Report Time'])
    # Extracting incidents that are within the timeframe
    urgent_datetime_alerts = report_times_df[
        report_times_df['report_datetime'] > datetime.now() - timedelta(hours=time_frame)]
    incident_id_set1 = set(urgent_datetime_alerts['Incident ID'].drop_duplicates().to_list())

    # Step 2: Keep incidents/alerts that occured on the same day, but have no Report time
    alerts_df['date'] = pd.to_datetime(alerts_df['Date'])

    # Filter by date
    # Remove alerts with no report time
    urgent_date_alerts = alerts_df[alerts_df['Report Time'].isna()]
    today_filter = urgent_date_alerts['date'].dt.date == datetime.now().date()
    urgent_date_alerts = urgent_date_alerts[today_filter]
    incident_id_set2 = set(urgent_date_alerts['Incident ID'].drop_duplicates().to_list())

    # Step 3: Joining two sets into all urgent ids
    urgent_inc_ids = incident_id_set1 | incident_id_set2

    # Step 4: Filtering original dataframe to alerts with urgent incident ids
    urgent_alerts_df = alerts_df[alerts_df['Incident ID'].isin(urgent_inc_ids)]

    urgent_alerts_df = urgent_alerts_df.drop(columns='date')

    return urgent_alerts_df


def filter_geodf(gdf, lat, lon, max_distance=10):
    """
    Given a latitude and longitude, returns a geopandas
    dataframe with the closest street objects within the
    given `max_distance` in meters.

    Parameters
    ----------
    gdf : Geopandas dataframe
        The geopandas dataframe with the streets
        data geometries
    lat : float
        latitude of the location of the alert
    long : float
        longitude of the location of the alert
    max_distance: int (default=10)
        The max distance of streets from the point
        in meters

    Returns
    -------
    gdf : Geopandas dataframe
        The filtered geopandas dataframe with
        only the streets that are within `max_distance`
        meters of the given `lat` and `lon` sorted by
        the distance column.
        Relevant Columns:
            - UNITDESC (object) : Full description of street
            - STNAME_ORD (object) : Street name
            - XSTRLO (object) : Street lower bound
            - XSTRHI (object) : Street upper bound
            - INTRLO (object) : Street lower intersection
            - INTRHI (object) : Street upper intersection
            - geometry (geometry) : shapely geometry object
            - distance (float64) : distance in meters from the point
    """

    if not isinstance(gdf, type(gpd.GeoDataFrame())):
        raise TypeError("gdf must be a geopandas.GeoDataFrame")
    if (lat > 90) | (lat < -90) | (lon <-180) | (lon > 180):
        raise ValueError("""invalid lat, lon combination, outside of valid bounds:\n
            lat:[-90,90]\n
            lon:[-180,180]""")

    # Point of interest
    alert_point = Point([lon, lat])

    # Define transformation
    project = pyproj.Transformer.from_proj(
        pyproj.Proj("EPSG:4326"),
        pyproj.Proj("EPSG:32610"), always_xy=True)

    # Projecting point
    projected_alert_point = transform(project.transform, alert_point)

    distances = []
    for street in gdf.geometry:
        # Projecting each linestring
        projected_street = transform(project.transform, street)
        # find the nearest points on the line and point geometries
        nearest_point_on_line, nearest_point_on_point = nearest_points(projected_street,
            projected_alert_point)
        # calculate the distance between the two nearest points
        distance = nearest_point_on_line.distance(nearest_point_on_point)
        distances.append(distance)

    gdf['distance'] = distances
    gdf = gdf.sort_values('distance')
    gdf = gdf[gdf['distance'] < max_distance]

    return gdf

def get_folium_map(alert_df):
    """
    Given information about alerts, return a rendered html leaflet map of the U-district area.

    Parameters
    ----------
    alert_df : pandas DataFrame containing our "database" of alerts
        Relevant Columns:
            - Nearest Address to Incident: str - The closest intersection to the incident
                origin derived from Chat GPT analysis
            - Incident Category: str - The type of incident derived from Chat GPT analysis
            - Incident Alert: str - The incident alert derived from the UW Alerts blog
            - Geometry: dict
                - The "location" key contains a coordinate pair value

    Returns
    -------
    m_html : str
        A rendered html leaflet map to display on the web application.
    """
    # alert_df exceptions
    # pylint: disable=line-too-long
    if not isinstance(alert_df, pd.DataFrame):
        raise TypeError("alert_df must be a pandas DataFrame")
    for col in ["Incident Category", "Incident Alert", "Nearest Address to Incident", "geometry"]:
        if col not in alert_df.columns:
            raise ValueError("""alert_df must have the following columns: Incident Category,
                                Incident Alert, Nearest Address to Incident, geometry""")

    # Display the U-District area
    gdf = gpd.read_file(os.path.join(os.path.dirname(__file__), "../data/SeattleGISData/udistrict_streets.geojson"))
    mapbox_api_key = 'pk.eyJ1IjoiZXZhbnlpcCIsImEiOiJjbGRxYnc3dXEwNWxxM25vNjRocHlsOHFyIn0.0H4RiKd8X94CeoXwEd4TgQ'
    html_map = folium.Map(location=[47.66, -122.32],
                          zoom_start=15,
                          tiles = f"https://api.mapbox.com/styles/v1/mapbox/dark-v11/tiles/512/{{z}}/{{x}}/{{y}}@2x?access_token={mapbox_api_key}",
                          attr="Maptiler Dark")

    alert_coords = [list(loc["location"].values()) for loc in alert_df["geometry"]]
    alert_categories = list(alert_df["Incident Category"])
    alert_nearest_intersections = list(alert_df["Nearest Address to Incident"])

    for i, coord in enumerate(alert_coords):
        # Display streets that are close to the alert
        filtered_streets = filter_geodf(gdf, coord[0], coord[1])
        folium.Choropleth(
            geo_data=filtered_streets,
            line_weight=3,
            line_color='red',
            line_opacity=0.5
        ).add_to(html_map)

        # Set a marker with an interactive popup
        iframe = folium.IFrame("<center><h4>" + str(alert_categories[i]) + "</h4><p style=\"font-family:Georgia, serif\">" + str(alert_nearest_intersections[i]) + "</p></center>")
        marker = folium.Marker(
            coord,
            popup=folium.Popup(iframe, min_width=200, max_width=250),
            icon=folium.Icon(color = "red", icon="circle-exclamation", prefix="fa")
        )
        marker.add_to(html_map)

    # Create a heatmap layer for each alert
    HeatMap(alert_coords, radius=10, gradient = {0: 'blue', 0.5: 'red'}).add_to(html_map)

    return html_map.get_root().render()
