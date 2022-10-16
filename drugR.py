import pandas as pd
import streamlit as st
import numpy as np

# import pandas_bokeh
# import matplotlib.pyplot as plt
import pgeocode
import pydeck as pdk
# import geopandas as gpd
# from shapely.geometry import Point
# from geopandas import GeoDataFrame
# pandas_bokeh.output_notebook()
# import plotly.graph_objects as go

df = pd.read_excel("Sampl.xlsx", header=13)

df = df.rename(columns={'Participant ID ': 'PID', 'Zip Code': 'ZipCode', 'Needles Distributed (Total Individual Needles)': 'Needles'})
df = df.rename(columns={'Naloxone Distributed (DOSES)':'Naloxone','Have You Ever Used Naloxone on Someone Else?': 'UseN' })
df = df.rename(columns={'(If no or hesistant) Would you like to be trained?': 'Train', 'Name of Recorder:': 'Recorder'})
df = df.rename(columns={'How many of those overdoses were successfully reversed?': 'SuccessR', 'How many overdoses have you responded to with Naloxone IN THE LAST 2 WEEKS? (# of people, NOT doses)': 'OverDoseResponse'})

df['OverDoseResponse'] = df['OverDoseResponse'].fillna(0)
df['SuccessR'] = df['SuccessR'].fillna(0)
df['UseN'] = df['UseN'].fillna('N')
df['Train'] = df['Train'].fillna('N')
df['Recorder'] = df['Recorder'].fillna('NotRecorded')

df['OverDoseResponse'] = df['OverDoseResponse'].astype(int)
df['SuccessR'] = df['SuccessR'].astype(int)

df.at[0, 'ZipCode'] = 92092

uniquePID = df.PID.nunique()
totalNeedles = df['Needles'].sum()
totalNaloxone = df['Naloxone'].sum()
trainResponse = df['UseN'].value_counts()
overdoseR = df['OverDoseResponse'].sum()
overdoseSuccess = df['SuccessR'].sum()
userDetails = df['PID'].value_counts()
#.to_dict()

# for key, value in userDetails.items():
#     print(key, value)

userDetails.columns = ['PIDs', 'Number of Interaction']
st.title("Demo Working")

st.header("Getting the basic info")
st.write("Number of Unique Participants:", uniquePID)
st.write("Total Number of Needles provided:", totalNeedles)
st.write("Total Number of Naloxone;", totalNaloxone)
st.write("Number of OverDose responses", overdoseR)
st.write("Overdose Response success:", overdoseSuccess)

st.header('Interactions with users')
st.table(userDetails)


df['ZipCode'] = df['ZipCode'].astype(str)

nomi = pgeocode.Nominatim('us')

df['latitude'] = (nomi.query_postal_code(df['ZipCode'].tolist()).latitude)
df['longitude'] = (nomi.query_postal_code(df['ZipCode'].tolist()).longitude)

df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

midpoint = (np.average(df['latitude']), np.average(df['longitude']))


st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=midpoint[0],
         longitude=midpoint[1],
         zoom=11,
         pitch=100,
     ),
     layers=[
        #  pdk.Layer(
        #     'HexagonLayer',
        #     data=df,
        #     get_position='[longitude, latitude]',
        #     radius=200,
        #     elevation_scale=5,
        #     elevation_range=[0, 3000],
        #     pickable=True,
        #     extruded=True,
        #  ),
        #  pdk.Layer(
        #      'ScatterplotLayer',
        #      data=df,
        #      get_position='[longitude, latitude]',
        #      get_color='[200, 30, 0, 160]',
        #      get_radius=200,
        #  ),
        pdk.Layer(
        "HeatmapLayer",
        df,
        opacity=0.9,
        get_position=["longitude", "latitude"]),
     ],
 ))

dft = pd.DataFrame(
     df,
     columns=['latitude', 'longitude'])

st.map(df)


# st.pydeck_chart(
#             viewport={
#                 'latitude': midpoint[0],
#                 'longitude':  midpoint[1],
#                 'zoom': 4
#             },
#             layers=[{
#                 'type': 'ScatterplotLayer',
#                 'data': df,
#                 'radiusScale': 250,
#    'radiusMinPixels': 5,
#                 'getFillColor': [248, 24, 148],
#             }]
#         )


# fig = go.Figure(data=go.Scattergeo(
#         lon = df['longitude'],
#         lat = df['latitude'],
#         users = df['PID'],
#         mode = 'markers',
#                 # marker_color = df['count'],
#         ))

# fig.update_layout(
#         title = 'User Distribution',
#         geo_scope='usa',
#     )

# st.plotly_chart(fig, use_container_width=True)
