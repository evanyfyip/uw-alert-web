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

import geopandas as gpd
import folium

    

def filter_geodf(gdf, lat, lon):
    """
    Given a latitude and longitude, returns a geopandas
    dataframe with the closest street object to that location

    Parameters
    ----------
    lat : float
        latitude of the location of the alert
    long : float
        longitude of the location of the alert
    
    gdf : Geopandas dataframe

    Returns
    -------
    geopandas Dataframe
        _description_
    """
    # TODO: Evan will work on this function
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
    mapbox_api_key = 'pk.eyJ1IjoiZXZhbnlpcCIsImEiOiJjbGRxYnc3dXEwNWxxM25vNjRocHlsOHFyIn0.0H4RiKd8X94CeoXwEd4TgQ'
    tileset_ID_str = "dark-v11"
    tilesize_pixels = "512"
    tile = f"https://api.mapbox.com/styles/v1/mapbox/{tileset_ID_str}/tiles/{tilesize_pixels}/{{z}}/{{x}}/{{y}}@2x?access_token={mapbox_api_key}"
    m = folium.Map(location=[47.66, -122.32], 
                    zoom_start=15, 
                    tiles = tile, 
                    attr="Maptiler Dark")
    folium.Choropleth(
        geo_data=gdf,
        line_weight=2,
        line_color='red'
    ).add_to(m)

    m_html = m.get_root().render()
    return m_html

def main():
    pass

if __name__ == '__main__':
    main()