#!/usr/bin/env python3

import os
import sys
import argparse
import requests
import pandas as pd
import folium
from folium.plugins import HeatMap


def get_nasa_firms_data(api_key, area, satellite='MODIS_NRT', time_window=10):
    """
    Fetches wildfire data from NASA's FIRMS API.

    :param api_key: NASA API key.
    :param area: Geographic area in "lon_min,lat_min,lon_max,lat_max" format.
    :param satellite: Satellite data to use (default is MODIS_NRT).
    :param time_window: Time window in days (default is 10).
    :return: CSV content of the wildfire data.
    """
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/{satellite}/{area}/{time_window}"
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch data: {response.content.decode('utf-8')}")
    return response.content


def save_data_to_csv(data_content, filename):
    """
    Saves the data content to a CSV file.

    :param data_content: Content to be written to the file.
    :param filename: Name of the file to write to.
    """
    with open(filename, 'wb') as f:
        f.write(data_content)


def load_data(filename):
    """
    Loads data from a CSV file into a pandas DataFrame.

    :param filename: Name of the CSV file to read from.
    :return: pandas DataFrame containing the data.
    """
    return pd.read_csv(filename)


def create_heatmap(df, output_filename, highlight_coords=None, highlight_popup=None):
    """
    Creates a heatmap from the wildfire data.

    :param df: DataFrame containing wildfire data.
    :param output_filename: Name of the output HTML file.
    :param highlight_coords: Coordinates to highlight on the map.
    :param highlight_popup: Popup text for the highlighted coordinates.
    """
    map_center = [df['latitude'].mean(), df['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=6)

    # Add heatmap layer
    heat_data = df[['latitude', 'longitude']].values.tolist()
    HeatMap(heat_data).add_to(m)

    # Add markers with popups
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3,
            popup=(
                f"Brightness: {row['brightness']}\n"
                f"Date: {row['acq_date']}"
            ),
            color='red',
            fill=True,
            fill_color='red'
        ).add_to(m)

    # Highlight specific coordinates if provided
    if highlight_coords and highlight_popup:
        folium.Marker(
            location=highlight_coords,
            popup=highlight_popup,
            icon=folium.Icon(color='blue')
        ).add_to(m)

    # Save the map
    m.save(output_filename)


def parse_arguments():
    """
    Parses command-line arguments.

    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Generate a heatmap of wildfire data from NASA FIRMS.'
    )
    parser.add_argument(
        '--api-key',
        default=os.getenv('NASA_API_KEY'),
        help='NASA API key (default: from NASA_API_KEY environment variable)'
    )
    parser.add_argument(
        '--area',
        default='-124.3,32.35,-114,42',
        help='Geographic area in "lon_min,lat_min,lon_max,lat_max" format (default: California)'
    )
    parser.add_argument(
        '--satellite',
        default='MODIS_NRT',
        help='Satellite data to use (e.g., MODIS_NRT, VIIRS_SNPP_NRT) (default: MODIS_NRT)'
    )
    parser.add_argument(
        '--time-window',
        type=int,
        default=10,
        help='Time window in days (default: 10)'
    )
    parser.add_argument(
        '--output',
        default='wildfires_heatmap.html',
        help='Output HTML file for the heatmap (default: wildfires_heatmap.html)'
    )
    parser.add_argument(
        '--highlight-coords',
        help='Coordinates to highlight, format "lat,lon" (optional)'
    )
    parser.add_argument(
        '--highlight-popup',
        help='Popup text for highlighted coordinates (optional)'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    if not args.api_key:
        print("Error: NASA API key not provided. Use --api-key or set NASA_API_KEY environment variable.")
        sys.exit(1)

    try:
        # Fetch and save data
        data_content = get_nasa_firms_data(
            api_key=args.api_key,
            area=args.area,
            satellite=args.satellite,
            time_window=args.time_window
        )
        csv_filename = 'fires.csv'
        save_data_to_csv(data_content, csv_filename)

        # Load data
        df = load_data(csv_filename)

        # Parse highlight coordinates if provided
        highlight_coords = None
        if args.highlight_coords:
            lat_str, lon_str = args.highlight_coords.split(',')
            highlight_coords = [float(lat_str), float(lon_str)]

        # Create heatmap
        create_heatmap(
            df=df,
            output_filename=args.output,
            highlight_coords=highlight_coords,
            highlight_popup=args.highlight_popup
        )

        print(f"Heatmap successfully saved to '{args.output}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
