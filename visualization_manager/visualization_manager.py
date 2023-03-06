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

def get_folium_map(alert_coords, alert_messages):
    """
    Given information about alerts, return a rendered html leaflet map of the U-district area.

    Parameters
    ----------
    alert_coords : List of List containing two Floats
        A list of coordinates [lat, long]
        representing alert locations
    alert_messages : List of Str
        Must be the same length as alert_coords
        A list of alert descriptions corresponding to alert_coords
        
    Returns
    -------
    m_html : str
        A rendered html leaflet map to display on the web application.
    """

    # alert_coords exceptions
    for alert in alert_coords:
        if not isinstance(alert, list) or len(alert) != 2:
            raise ValueError("alert_coords must contain Lists of length 2")
        if not isinstance(alert[0], (int, float)) or not isinstance(alert[1], (int, float)):
            raise ValueError("coordinates in alert_coords must contain numbers")

    # alert_messages exceptions
    if not isinstance(alert_messages, list) or len(alert_messages) != len(alert_coords):
        raise ValueError("alert_messages must be a list with the same length as alert_coords")
    if any([True for alert in alert_messages if not isinstance(alert, str)]):
        raise ValueError("alert_messages must only contain strings")

    # Display the U-District area
    gdf = gpd.read_file('./data/SeattleGISData/udistrict_streets.geojson')
    # pylint: disable=line-too-long
    mapbox_api_key = 'pk.eyJ1IjoiZXZhbnlpcCIsImEiOiJjbGRxYnc3dXEwNWxxM25vNjRocHlsOHFyIn0.0H4RiKd8X94CeoXwEd4TgQ'
    tileset_id_str = "dark-v11"
    tilesize_pixels = "512"
    tile = f"https://api.mapbox.com/styles/v1/mapbox/{tileset_id_str}/tiles/{tilesize_pixels}/{{z}}/{{x}}/{{y}}@2x?access_token={mapbox_api_key}"
    map = folium.Map(location=[47.66, -122.32],
                    zoom_start=15,
                    tiles = tile,
                    attr="Maptiler Dark")
    # Highlight the streets in U-District
    # folium.Choropleth(
    #     geo_data=gdf,
    #     line_weight=2,
    #     line_color='red'
    # ).add_to(map)

    ## TODO: Implement different coloring based on the urgency of an alert
    for i in range(len(alert_coords)):
        # Display streets that are close to the alert
        filtered_streets = filter_geodf(gdf, alert_coords[i][0], alert_coords[i][1])
        folium.Choropleth(
            geo_data=filtered_streets,
            line_weight=3,
            line_color='blue'
        ).add_to(map)

        # Set a marker with an interactive popup
        iframe = folium.IFrame("<b>" + alert_messages[i] + "</b>")
        popup = folium.Popup(iframe, min_width=300, max_width=300)
        folium.Marker(
            alert_coords[i],
            popup=popup
        ).add_to(map)
    # Create a heatmap layer for each alert
    HeatMap(alert_coords, radius=10, gradient = {0: 'blue', 0: 'lime', 0.5: 'red'}).add_to(map)

    m_html = map.get_root().render()
    return m_html
