from setuptools import setup, find_packages

setup(
    name="uw-alert-web",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pyproj',
        'folium==0.14.0',
        'shapely==2.0.1',
        'flask==2.2.2',
        'numpy==1.24.2',
        'pylint==2.16.2',
        'geopandas==0.12.2',
        'openai==0.26.5',
        'transformers==4.26.1',
        'requests==2.28.1',
        'bs4',
        'python-dotenv==0.21.0',
        'googlemaps==4.10.0',
    ],
)