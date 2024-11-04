import streamlit as st
import pandas as pd
import geopandas as gpd
import shapely
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import requests
import json
from shapely.geometry import shape

geojson = requests.get('https://archivo.habitat.gob.ar/dataset/ssisu/renabap-datos-barrios-geojson').json()

print(geojson)

filtered_data = [feature for feature in geojson['features'] if feature['properties']['provincia'] == 'Ciudad Autónoma de Buenos Aires']

features = []
for feature in filtered_data:
    geometry = shape(feature["geometry"])  # Convierte coordenadas a geometría de shapely
    properties = feature["properties"]
    properties["geometry"] = geometry
    features.append(properties)

gdf = gpd.GeoDataFrame(features)

gdf['id_temporal'] = gdf.index

fig = px.choropleth_mapbox(
    gdf,
    geojson=gdf.set_geometry("geometry").__geo_interface__,
    locations="id_temporal",
    hover_name="nombre_barrio",
    hover_data={
        'id_temporal': False,
        "cantidad_familias_aproximada": True
    },
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    center={"lat": -34.6159, "lon": -58.4358},  # Coordenadas aproximadas de Buenos Aires
    zoom=11,
    opacity=0.5,
)

st.plotly_chart(fig, use_container_width=True)