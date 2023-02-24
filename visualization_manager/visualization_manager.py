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

import pyproj
import folium
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import nearest_points, transform

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

def get_folium_map():
    """_summary_

    Parameters
    ----------
    gdf : _type_
        _description_

    Returns
    -------
    m_html : str
        
    """
    gdf = gpd.read_file('../data/SeattleGISData/udistrict_streets.geojson')
    # pylint: disable=line-too-long
    mapbox_api_key = 'pk.eyJ1IjoiZXZhbnlpcCIsImEiOiJjbGRxYnc3dXEwNWxxM25vNjRocHlsOHFyIn0.0H4RiKd8X94CeoXwEd4TgQ'
    tileset_id_str = "dark-v11"
    tilesize_pixels = "512"
    tile = f"https://api.mapbox.com/styles/v1/mapbox/{tileset_id_str}/tiles/{tilesize_pixels}/{{z}}/{{x}}/{{y}}@2x?access_token={mapbox_api_key}"
    map = folium.Map(location=[47.66, -122.32], 
                    zoom_start=15, 
                    tiles = tile, 
                    attr="Maptiler Dark")
    folium.Choropleth(
        geo_data=gdf,
        line_weight=2,
        line_color='red'
    ).add_to(map)

    m_html = map.get_root().render()
    return m_html
