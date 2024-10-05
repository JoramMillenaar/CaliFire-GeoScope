import os

import requests
import pandas as pd
import folium
from folium.plugins import HeatMap

# Get NASA API key from environment variable
api_key = os.getenv('NASA_API_KEY')
cal_area = '-124.3,32.35,-114,42'

# Check if the API key is available
if not api_key:
    raise ValueError("No API key found. Set the NASA_API_KEY environment variable.")

# URL for NASA FIRMS data (last 24 hours, California region)
url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/MODIS_NRT/{cal_area}/10"
response = requests.get(url)
if response.status_code != 200:
    print("Failed to fetch data:", response.content)
    exit()

with open('fires.csv', 'wb') as f:
    f.write(response.content)

# Step 2: Load data into DataFrame
df = pd.read_csv('fires.csv')

# Step 3: Create base map
map_center = [df['latitude'].mean(), df['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=6)

# Step 4: Add heatmap layer
heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

# Step 5: Add markers with popups
for index, row in df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=3,
        popup=f"Brightness: {row['brightness']}\nDate: {row['acq_date']}",
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

# Step 6: Highlight Redding, CA
redding_coords = [40.5865, -122.3917]
folium.Marker(
    location=redding_coords,
    popup='Redding, CA',
    icon=folium.Icon(color='blue')
).add_to(m)

# Step 7: Save the map
m.save('california_wildfires_heatmap.html')
