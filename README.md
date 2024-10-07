<p align="center">
    <img src="logo.webp" alt="logo" width="250" />
</p>

# California Wildfire Visualization

## Overview
This project provides a Python script to visualize recent wildfire data from NASA's Fire Information for Resource Management System (FIRMS) for California. The script fetches data using the MODIS and VIIRS satellites and generates an interactive heatmap that displays active wildfires. It includes a special focus on Redding, CA, highlighting the intensity and location of wildfires in the area.

<p align="center">
    <img src="example.png" alt="example heatmap" width="400" />
</p>

## Features
- **Real-Time Satellite Data**: Fetches the latest wildfire data from NASA's FIRMS API.
- **Heatmap Visualization**: Visualizes the intensity and distribution of wildfires across California.
- **Detailed Markers**: Displays detailed information about each wildfire, including brightness and detection date.
- **Customizable Focus**: Allows for highlighting specific areas, such as Redding, CA.
- **Command-Line Arguments**: Supports customization of parameters such as satellite data, area, time window, and more.

## Data Source
Data is sourced from NASA's FIRMS via MODIS and VIIRS satellites, providing near-real-time monitoring of global wildfires.

## Installation
Ensure Python 3.x is installed and set up:

### Dependencies
Install the required Python packages:
```bash
pip install pandas folium requests
```

### API Key
Obtain a NASA API key and set it as an environment variable:
```bash
export NASA_API_KEY='your_nasa_api_key_here'
```
You can generate an API key [here](https://api.nasa.gov/).

## Usage
Run the script with default parameters or customize the input:
```bash
python wildfire_heatmap.py
```
Customize parameters using command-line options:
```bash
python wildfire_heatmap.py --area="-124.3,32.35,-114,42" --satellite="VIIRS_SNPP_NRT" --time-window=7 --highlight-coords="40.5865,-122.3917" --highlight-popup="Redding, CA"
```

## Project Structure
- **wildfire_heatmap.py**: Main script to fetch data and generate the heatmap.
- **fires.csv**: Generated CSV file with the latest wildfire data.
- **california_wildfires_heatmap.html**: Generated interactive HTML map file.

## Contributing
Contributions are welcome to enhance the script's functionality or improve the visualization. Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- **NASA FIRMS**: For providing open access to fire data.
- **MODIS and VIIRS Satellite Teams**: For continuous monitoring and data provision.
